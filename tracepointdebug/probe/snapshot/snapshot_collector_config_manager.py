class DEFAULT_SNAPSHOT_CONFIGS:
    MAX_FRAMES = 10
    MAX_EXPAND_FRAMES = 1
    MAX_PROPERTIES = 10
    MAX_PARSE_DEPTH = 3
    MAX_VAR_LEN = 256
    MAX_SIZE = 32768

class MAX_SNAPSHOT_CONFIGS:
    MAX_FRAMES = 20
    MAX_EXPAND_FRAMES = 5
    MAX_PROPERTIES = 50
    MAX_PARSE_DEPTH = 6

snapshot_configs = {
    "maxFrames": DEFAULT_SNAPSHOT_CONFIGS.MAX_FRAMES,
    "maxExpandFrames": DEFAULT_SNAPSHOT_CONFIGS.MAX_EXPAND_FRAMES,
    "maxProperties": DEFAULT_SNAPSHOT_CONFIGS.MAX_PROPERTIES,
    "maxParseDepth": DEFAULT_SNAPSHOT_CONFIGS.MAX_PARSE_DEPTH,
    "maxVarLen": DEFAULT_SNAPSHOT_CONFIGS.MAX_VAR_LEN,
    "maxSize": DEFAULT_SNAPSHOT_CONFIGS.MAX_SIZE
}

class SnapshotCollectorConfigManager():

    @staticmethod
    def get_max_size():
        return snapshot_configs.get("maxSize")

    @staticmethod
    def get_max_var_len():
        return snapshot_configs.get("maxVarLen")

    @staticmethod
    def get_max_frames():
        return snapshot_configs.get("maxFrames")

    @staticmethod
    def get_max_expand_frames():
        return snapshot_configs.get("maxExpandFrames")
    
    @staticmethod
    def get_parse_depth():
        return snapshot_configs.get("maxParseDepth")
    
    @staticmethod
    def get_max_properties():
        return snapshot_configs.get("maxProperties")

    @staticmethod
    def update_snapshot_config(update_configs): 
        max_frames = update_configs.get("maxFrames", DEFAULT_SNAPSHOT_CONFIGS.MAX_FRAMES)
        max_expand_frames = update_configs.get("maxExpandFrames", DEFAULT_SNAPSHOT_CONFIGS.MAX_EXPAND_FRAMES)
        max_properties = update_configs.get("maxProperties", DEFAULT_SNAPSHOT_CONFIGS.MAX_PROPERTIES)
        max_parse_depth = update_configs.get("maxParseDepth", DEFAULT_SNAPSHOT_CONFIGS.MAX_PARSE_DEPTH)
        snapshot_configs["maxFrames"] = MAX_SNAPSHOT_CONFIGS.MAX_FRAMES if max_frames > MAX_SNAPSHOT_CONFIGS.MAX_FRAMES else max_frames
        snapshot_configs["maxExpandFrames"] = MAX_SNAPSHOT_CONFIGS.MAX_EXPAND_FRAMES if max_expand_frames > MAX_SNAPSHOT_CONFIGS.MAX_EXPAND_FRAMES else max_expand_frames
        snapshot_configs["maxProperties"] = MAX_SNAPSHOT_CONFIGS.MAX_PROPERTIES if max_properties > MAX_SNAPSHOT_CONFIGS.MAX_PROPERTIES else max_properties
        snapshot_configs["maxParseDepth"] = MAX_SNAPSHOT_CONFIGS.MAX_PARSE_DEPTH if max_parse_depth > MAX_SNAPSHOT_CONFIGS.MAX_PARSE_DEPTH else max_parse_depth