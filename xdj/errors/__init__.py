class LoadControllerError(Exception):
    def __init__(self, message,filepath, errors):
        # Call the base class constructor with the parameters it needs
        super(type(self),self).__init__("load {0} is error {1}".format(filepath, message))
        # Now for your custom code...
        self.errors = errors
class LoadConfigError(Exception):
    def __init__(self, message,filepath, errors):
        # Call the base class constructor with the parameters it needs
        super(type(self),self).__init__("load config {0} is error {1}".format(filepath, message))
        # Now for your custom code...
        self.errors = errors
