class ApplicationFilter:

    @property
    def name(self):
        return self._name


    @name.setter
    def name(self, name):
        self._name = name    

    
    @property
    def stage(self):
        return self._stage

    
    @stage.setter
    def stage(self, stage):
        self._stage = stage


    @property
    def version(self):
        return self._version


    @version.setter
    def version(self, version):
        self._version = version


    @property
    def custom_tags(self):
        return self._custom_tags

    
    @custom_tags.setter
    def custom_tags(self, custom_tags):
        self._custom_tags = custom_tags


    def to_json(self):
        return {
                "name": self.name,
                "stage": self.stage,
                "version": self.version,
                "customTags": self.custom_tags
            }