from selenium.common import exceptions as seleniumexceptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from seleniumdirector import exceptions
import time


class Expectation(object):
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        try:
            element = expected_conditions._find_element(driver, self.locator)
            return self.check(element)
        except seleniumexceptions.StaleElementReferenceException:
            return False


class text_to_be_present_in_element_contents_or_value(Expectation):
    """
    An expectation for checking if the given text is present in the element's
    text (e.g. for a div) or its value attribute (e.g. for an input box).
    """

    def check(self, element):
        if self.text in element.text:
            return True
        value_attr = element.get_attribute("value")
        if value_attr is not None:
            return self.text in value_attr
        return False


class WebElement(object):
    def __init__(self, director, name, page, xpath):
        self._director = director
        self.name = name
        self.page = page
        self.xpath = xpath

    @property
    def _element(self):
        try:
            return self._director.driver.find_element_by_xpath(self.xpath)
        except seleniumexceptions.NoSuchElementException:
            raise exceptions.ElementDidNotAppear((
                "Could not find '{}' on page '{}' using xpath '{}' "
                "after default timeout of {} seconds.").format(
                    self.name,
                    self.page,
                    self.xpath,
                    self._director.default_timeout,
                ))

    @property
    def element(self):
        return self._element

    @property
    def _selector(self):
        return (By.XPATH, self.xpath)

    def send_keys(self, keys):
        self.element.send_keys(keys)

    def click(self):
        self.element.click()

    def should_not_be_on_page(self, after=None):
        """
        Ensure element is either not present or that display:none is set after
        a specified duration.

        Specify 'after' to wait for a specific duration in seconds. By default
        it waits for default_timeout seconds.
        """
        timeout = after if after is not None else self._director.default_timeout
        try:
            WebDriverWait(
                self._director.driver, timeout
            ).until_not(
                expected_conditions.presence_of_element_located(self._selector)
            )
        except seleniumexceptions.TimeoutException:
            raise exceptions.ElementStillOnPage(
                "{} still on page after {} seconds.".format(
                    self.name,
                    timeout,
                )
            )

    def should_contain(self, text, after=None):
        timeout = after if after is not None else self._director.default_timeout
        start_time = time.time()
        self.should_be_on_page(after=after)
        continue_for_how_long = timeout - (time.time() - start_time)
        try:
            WebDriverWait(self._director.driver, continue_for_how_long).until(
                text_to_be_present_in_element_contents_or_value(self._selector, text)
            )
        except seleniumexceptions.TimeoutException:
            raise exceptions.ElementDidNotContain((
                "Element '{}' on page '{}' using xpath '{}' "
                "contained:\n\n{}\n\nnot:\n\n{}\n\nafter timeout of {} seconds.").format(
                    self.name,
                    self.page,
                    self.xpath,
                    self.element.text,
                    text,
                    timeout,
                ))

    def should_be_on_page(self, after=None):
        """
        Ensure is on the page and display:none is not set.

        Specify 'after' to wait for a specific duration in seconds. By default
        it waits for default_timeout seconds.
        """
        timeout = after if after is not None else self._director.default_timeout
        try:
            WebDriverWait(self._director.driver, timeout).until(
                expected_conditions.visibility_of_element_located(self._selector)
            )
        except seleniumexceptions.TimeoutException:
            raise exceptions.ElementDidNotAppear((
                "Could not find '{}' on page '{}' using xpath '{}' "
                "after timeout of {} seconds.").format(
                    self.name,
                    self.page,
                    self.xpath,
                    timeout,
                ))
        if len(self._director.driver.find_elements_by_xpath(self.xpath)) > 1:
            raise exceptions.MoreThanOneElement(
                "More than one element matches your query '{}'.".format(
                    self._selector[1]
                )
            )

    def should_be_on_top(self, after=None):
        """
        Waits for element to:

        * Be on the page (e.g. either just be there or put on to the DOM by javascript).
        * Not set to be invisible (i.e. display:none isn't set).
        * Not be covered by another element (e.g. an overlay).

        The element's midpoint is checked to see if it is covered. It does not matter
        if corners are covered.

        Specify 'after' to wait for a specific duration in seconds. By default
        it waits for default_timeout seconds.
        """
        start_time = time.time()
        self.should_be_on_page(after=after)
        timeout = after if after is not None else self._director.default_timeout
        continue_for_how_long = timeout - (
            time.time() - start_time
        )

        for i in range(0, int(continue_for_how_long * 10.0)):
            element_coordinates = self.element.location
            element_size = self.element.size
            element_at_coordinates = self._director.driver.execute_script(
                "return document.elementFromPoint({}, {})".format(
                    element_coordinates["x"] + element_size['width'] / 2,
                    element_coordinates["y"] + element_size['height'] / 2,
                )
            )
            if self.element.id == element_at_coordinates.id:
                break
            time.sleep(0.1)

        total_duration = time.time() - start_time

        if total_duration > timeout:
            raise exceptions.ElementCoveredByAnotherElement((
                    "Another element, a '{}' with id '{}' "
                    "and class '{}' is covering yours '{}'."
                ).format(
                    element_at_coordinates.tag_name,
                    element_at_coordinates.get_attribute("id"),
                    element_at_coordinates.get_attribute("class"),
                    self._selector[1],
                )
            )
