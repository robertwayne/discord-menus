class MenuException(Exception):
    def __init__(self, message: str = None):
        self.message = message


class PagesError(MenuException):
    pass


class ButtonsError(MenuException):
    pass


class EventError(MenuException):
    pass


class SessionError(MenuException):
    pass


class TooManyButtonsWarning(MenuException):
    pass
