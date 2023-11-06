import _thread

class ValoraExpiredException(Exception):
    def __init__(self, msg=None):
        self.msg = msg

class ValoraLoginFailedException(Exception):
    def __init__(self, msg=None):
        self.msg = msg

class ValoraCacheUpdateFailedException(Exception):
    def __init__(self, msg=None, func=None):
        self.msg = msg
        if func:
            _thread.start_new_thread(func, ())