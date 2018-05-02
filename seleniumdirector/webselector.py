from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from strictyaml import load, MapPattern, Str, Map
from selenium.webdriver.common.by import By
from path import Path



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
        return self.text in element.text or self.text in element.get_attribute("value")



class WebElement(object):
    def __init__(self, director, sel_type, identifier):
        self._director = director
        self.sel_type = sel_type
        self.identifier = identifier

    @property
    def _element(self):
        return self._director.driver.find_element_by_id(self.identifier)

    def send_keys(self, keys):
        self._element.send_keys(keys)

    def click(self):
        self._element.click()

    def should_contain(self, text):
        WebDriverWait(self._director.driver, self._director.default_timeout).until(
            text_to_be_present_in_element_contents_or_value(
                (By.CSS_SELECTOR, "#{0}".format(self.identifier)), text
            )
        )



class WebSelector(object):
    def __init__(self, driver, selector_file):
        self.driver = driver
        self._selectors = load(
            Path(selector_file).text(),
            MapPattern(
                Str(),
                Map({
                    "appears when": Str(),
                    "elements": MapPattern(Str(), Str()),
                }),
            )
        ).data
        self._current_page = None
        self.default_timeout = 5

    def visit(self, url):
        self.driver.get(url)

    def wait_for_page(self, page_name):
        WebDriverWait(self.driver, self.default_timeout).until(
            expected_conditions.visibility_of_element_located(
                self._page_selector(page_name)
            )
        )
        self._current_page = page_name

    def _page_selector(self, page_name):
        seltype, ident = self._selectors[page_name]['appears when'].split("=")
        return (By.CSS_SELECTOR, "#{0}".format(ident))

    def the(self, name):
        seltype, ident = self._selectors[self._current_page]['elements'][name].split("=")
        return WebElement(self, seltype, ident)
