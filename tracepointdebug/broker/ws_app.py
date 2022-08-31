import threading
import time

import six
from websocket import WebSocketApp, WebSocketException, WebSocket, ABNF, WebSocketTimeoutException


class WSApp(WebSocketApp):
    def run_forever(self, sockopt=None, sslopt=None,
                    ping_interval=0, ping_timeout=None,
                    http_proxy_host=None, http_proxy_port=None,
                    http_no_proxy=None, http_proxy_auth=None,
                    skip_utf8_validation=False,
                    host=None, origin=None, dispatcher=None,
                    suppress_origin=False, proxy_type=None, timeout=None):
        if ping_timeout is not None and ping_timeout <= 0:
            ping_timeout = None
        if ping_timeout and ping_interval and ping_interval <= ping_timeout:
            raise WebSocketException("Ensure ping_interval > ping_timeout")
        if not sockopt:
            sockopt = []
        if not sslopt:
            sslopt = {}
        if self.sock:
            raise WebSocketException("socket is already opened")
        thread = None
        self.keep_running = True
        self.last_ping_tm = 0
        self.last_pong_tm = 0

        def teardown(close_frame=None):
            """
            Tears down the connection.
            If close_frame is set, we will invoke the on_close handler with the
            statusCode and reason from there.
            """
            if thread and thread.isAlive():
                event.set()
                thread.join()
            self.keep_running = False
            if self.sock:
                self.sock.close()
            close_args = self._get_close_args(
                close_frame.data if close_frame else None)
            self._callback(self.on_close, *close_args)
            self.sock = None

        try:
            self.sock = WebSocket(
                self.get_mask_key, sockopt=sockopt, sslopt=sslopt,
                fire_cont_frame=self.on_cont_message is not None,
                skip_utf8_validation=skip_utf8_validation,
                enable_multithread=True if ping_interval else False)
            self.sock.settimeout(timeout)
            self.sock.connect(
                self.url, header=self.header, cookie=self.cookie,
                http_proxy_host=http_proxy_host,
                http_proxy_port=http_proxy_port, http_no_proxy=http_no_proxy,
                http_proxy_auth=http_proxy_auth, subprotocols=self.subprotocols,
                host=host, origin=origin, suppress_origin=suppress_origin,
                proxy_type=proxy_type)
            if not dispatcher:
                dispatcher = self.create_dispatcher(ping_timeout)

            self._callback(self.on_open)

            if ping_interval:
                event = threading.Event()
                thread = threading.Thread(
                    target=self._send_ping, args=(ping_interval, event, None))
                thread.setDaemon(True)
                thread.start()

            def read():
                if not self.keep_running:
                    return teardown()

                op_code, frame = self.sock.recv_data_frame(True)
                if op_code == ABNF.OPCODE_CLOSE:
                    return teardown(frame)
                elif op_code == ABNF.OPCODE_PING:
                    self._callback(self.on_ping, frame.data)
                elif op_code == ABNF.OPCODE_PONG:
                    self.last_pong_tm = time.time()
                    self._callback(self.on_pong, frame.data)
                elif op_code == ABNF.OPCODE_CONT and self.on_cont_message:
                    self._callback(self.on_data, frame.data,
                                   frame.opcode, frame.fin)
                    self._callback(self.on_cont_message,
                                   frame.data, frame.fin)
                else:
                    data = frame.data
                    if six.PY3 and op_code == ABNF.OPCODE_TEXT:
                        data = data.decode("utf-8")
                    self._callback(self.on_data, data, frame.opcode, True)
                    self._callback(self.on_message, data)

                return True

            def check():
                if (ping_timeout):
                    has_timeout_expired = time.time() - self.last_ping_tm > ping_timeout
                    has_pong_not_arrived_after_last_ping = self.last_pong_tm - self.last_ping_tm < 0
                    has_pong_arrived_too_late = self.last_pong_tm - self.last_ping_tm > ping_timeout

                    if (self.last_ping_tm
                            and has_timeout_expired
                            and (has_pong_not_arrived_after_last_ping or has_pong_arrived_too_late)):
                        raise WebSocketTimeoutException("ping/pong timed out")
                return True

            dispatcher.read(self.sock.sock, read, check)
        except (Exception, KeyboardInterrupt, SystemExit) as e:
            self._callback(self.on_error, e)
            if isinstance(e, SystemExit):
                # propagate SystemExit further
                raise
            teardown()
            return not isinstance(e, KeyboardInterrupt)
