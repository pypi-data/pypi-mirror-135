import dizest as sd

class config:
    def __init__(self, **kwargs):
        self.data = sd.util.stdClass(**kwargs)
        
        self.defaults = sd.util.stdClass()
        self.defaults.cache = "memory"
        self.defaults.logger = print

    def __getattr__(self, key):
        def fn(value=None):
            if value is None:
                value = self.data[key]
                if value is None:
                    value = self.defaults[key]
                return value

            self.data[key] = value
            return self.data[key]
        return fn

    def get(self, key):
        return self.__getattr__(key)()

    def set(self, key, value):
        return self.__getattr__(key)(value)

    def delete(self, key):
        del self.data[key]

