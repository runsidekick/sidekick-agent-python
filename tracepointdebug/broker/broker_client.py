import logging
import socket
import threading
from threading import Thread
from time import sleep

import websocket

from tracepointdebug.utils import debug_logger
from tracepointdebug.broker.ws_app import WSApp
from tracepointdebug.application.application import Application

logger = logging.getLogger(__name__)

_TIMEOUT = 3
OPCODE_BINARY = 0x2
BROKER_HANDSHAKE_HEADERS = {
    "API_KEY": "x-sidekick-api-key",
    "APP_INSTANCE_ID": "x-sidekick-app-instance-id",
    "APP_NAME": "x-sidekick-app-name",
    "APP_VERSION": "x-sidekick-app-version",
    "APP_STAGE": "x-sidekick-app-stage",
    "APP_RUNTIME": "x-sidekick-app-runtime",
    "APP_HOSTNAME": "x-sidekick-app-hostname"
}
APP_TAG_HEADER_NAME_PREFIX = "x-sidekick-app-tag-"

class BrokerConnection:

    def __init__(self, host, port, broker_credentials, message_callback, initial_request_to_broker):
        self.message_callback = message_callback
        self.host = host
        self.port = port
        self.broker_credentials = broker_credentials
        self.ws = None
        self._thread = None
        self._running = False
        self.connection_timer = None
        self.connection_timeout = 10
        self.reconnect_interval = 3
        self.connected = threading.Event()
        self.initial_request_to_broker = initial_request_to_broker

    def is_running(self):
        return self._running

    def _create_app(self):
        return WSApp(
            self.get_broker_url(self.host, self.port),
            on_message=lambda ws, msg: self.on_message(ws, msg),
            on_error=lambda ws, msg: self.on_error(ws, msg),
            on_close=lambda ws: self.on_close(ws),
            on_open=lambda ws: self.on_open(ws),
            on_ping=lambda ws, msg: self.on_ping(ws, msg),
            on_pong=lambda ws, msg: self.on_pong(ws, msg),
            header= self._create_wsapp_header()
            
        )

    def _create_wsapp_header(self):
        header=[
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("API_KEY"),
                                           value=self.broker_credentials.api_key),
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("APP_INSTANCE_ID"),
                                           value=self.broker_credentials.app_instance_id),
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("APP_NAME"),
                                           value=self.broker_credentials.app_name),
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("APP_VERSION"),
                                           value=self.broker_credentials.app_version),
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("APP_STAGE"),
                                           value=self.broker_credentials.app_stage),
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("APP_RUNTIME"),
                                           value=self.broker_credentials.runtime),
                "{header}: {value}".format(header=BROKER_HANDSHAKE_HEADERS.get("APP_HOSTNAME"),
                                           value=self.broker_credentials.hostname)
            ]

        application_info = Application.get_application_info()
        application_tags = application_info.get("applicationTags", {})
        if application_tags:
            for appTagName, appTagValue in application_tags.items():
                header.append(
                    "{header}: {value}".format(header=APP_TAG_HEADER_NAME_PREFIX + appTagName,
                                            value=appTagValue
                ))

        return header

    def _connect(self):
        self.ws = self._create_app()
        debug_logger("Connecting to broker...")
        self.ws.run_forever(ping_interval=60, ping_timeout=10,
                            sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),))

        while self._running:
            debug_logger("Reconnecting in %s..." % self.reconnect_interval)
            sleep(self.reconnect_interval)
            debug_logger("Connecting to broker...")
            self.ws = self._create_app()
            self.ws.run_forever(ping_interval=60, ping_timeout=10,
                                sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),), timeout=self.connection_timeout)

    def connect(self):
        self._running = True
        import sys
        if sys.version_info[0] >= 3:
            self._thread = Thread(target=self._connect, daemon=True)
        else:
            self._thread = Thread(target=self._connect)
            self._thread.daemon = True
        self._thread.start()

    @staticmethod
    def get_broker_url(host, port):
        if host.startswith("ws://") or host.startswith("wss://"):
            return host + ":" + str(port) + "/app"
        else:
            return "wss://" + host + ":" + str(port) + "/app"

    def on_ping(self, ws, msg):
        debug_logger("Sending ping...")

    def on_pong(self, ws, msg):
        debug_logger("Got pong...")

    def on_message(self, ws, msg):
        self.message_callback(self, msg)

    def on_error(self, ws, msg):
        if isinstance(msg, websocket.WebSocketBadStatusException):
            logger.error("Handshake failed, status code: {}, message: {}".format(msg.status_code, msg.args))
            if msg.status_code == 401:
                self._running = False
                if self.ws:
                    self.ws.close()
        logger.error("Error on connection, msg: {}".format(msg))

    def on_close(self, ws):
        debug_logger("Connection closed")

    def on_open(self, ws):
        debug_logger("Connection open")
        self.connected.set()
        connection_set = self.connected.wait() #TODO Timeout
        if connection_set:
            self.initial_request_to_broker()

    def send(self, data):
        try:
            self.ws.send(data)
        except websocket.WebSocketConnectionClosedException as e:
            logger.error("Error sending %s" % e)

    def close(self):
        self._running = False
        if self.ws:
            self.ws.close()
        self._thread.join()
