class Config:
    def __init__(self ,**kwargs):
        self._values=kwargs

    def get(self,key,default=None):
        return self._values.get(key,default)