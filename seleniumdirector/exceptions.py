class SeleniumDirectorException(Exception):
    pass


class MoreThanOneElement(SeleniumDirectorException):
    pass


class ElementCoveredByAnotherElement(SeleniumDirectorException):
    pass


class NotFoundInSelectors(SeleniumDirectorException):
    pass


class ElementDidNotAppear(SeleniumDirectorException):
    pass


class ElementDidNotContain(SeleniumDirectorException):
    pass


class ElementStillOnPage(SeleniumDirectorException):
    pass
