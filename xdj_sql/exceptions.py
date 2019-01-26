class RequireValue(Exception):
    def __init__(self,message,fields):
        super(RequireValue,self).__init__(message)
        self.fields = fields
