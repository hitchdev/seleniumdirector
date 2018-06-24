from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from seleniumdirector import exceptions


class Expectation(object):
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        try:
            element = expected_conditions._find_element(driver, self.locator)
            return self.check(element)
        except StaleElementReferenceException:
            return False


class text_to_be_present_in_element_contents_or_value(Expectation):
    """
    An expectation for checking if the given text is present in the element's
    text or its value attribute.
    """

    def check(self, element):
        if self.text in element.text:
            return True
        value_attr = element.get_attribute("value")
        if value_attr is not None:
            return self.text in value_attr
        return False


class WebElement(object):
    def __init__(self, director, sel_type, identifier):
        self._director = director
        self.sel_type = sel_type
        self.identifier = identifier

    @property
    def _element(self):
        if self.sel_type == "id":
            return self._director.driver.find_element_by_id(self.identifier)
        elif self.sel_type == "xpath":
            return self._director.driver.find_element_by_xpath(self.identifier)

    @property
    def _selector(self):
        if self.sel_type == "id":
            return (By.XPATH, "//*[@id='{0}']".format(self.identifier))
        elif self.sel_type == "xpath":
            return (By.XPATH, self.identifier)

    def send_keys(self, keys):
        self._element.send_keys(keys)

    def click(self):
        self._element.click()

    def should_contain(self, text):
        WebDriverWait(self._director.driver, self._director.default_timeout).until(
            text_to_be_present_in_element_contents_or_value(self._selector, text)
        )

    def should_appear(self):
        WebDriverWait(self._director.driver, self._director.default_timeout).until(
            expected_conditions.visibility_of_element_located(self._selector)
        )
        if len(self._director.driver.find_elements_by_xpath(self.identifier)) > 1:
            raise exceptions.MoreThanOneElement(
                "More than one element matches your query '{}'.".format(self.identifier)
            )
