class SearchException(Exception):

    def __init__(self, code, message, detail_error=None):
        self.code = code
        self.message = message
        self.detail_error = detail_error

