class SeleniumDirectorException(Exception):
    pass


class MoreThanOneElement(SeleniumDirectorException):
    pass


class ElementCoveredByAnotherElement(SeleniumDirectorException):
    pass


class NotFoundInSelectors(SeleniumDirectorException):
    pass
