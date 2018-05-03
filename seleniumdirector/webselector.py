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
        if self.sel_type == "id":
            return self._director.driver.find_element_by_id(self.identifier)
        elif self.sel_type == "xpath":
            return self._director.driver.find_element_by_xpath(self.identifier)

    @property
    def _selector(self):
        if self.sel_type == "id":
            return (By.CSS_SELECTOR, "#{0}".format(self.identifier))
        elif self.sel_type == "xpath":
            return (By.XPATH, self.identifier)

    def send_keys(self, keys):
        self._element.send_keys(keys)

    def click(self):
        self._element.click()

    def should_contain(self, text):
        WebDriverWait(self._director.driver, self._director.default_timeout).until(
            text_to_be_present_in_element_contents_or_value(
                self._selector, text
            )
        )

    def should_appear(self):
        WebDriverWait(self._director.driver, self._director.default_timeout).until(
            expected_conditions.visibility_of_element_located(
                self._selector
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
                    "appears when": Map({"attribute": Str()}) | Str(),
                    "elements": MapPattern(
                        Str(),
                        Str() | Map({"attribute": Str()}) | Map({"xpath": Str()}),
                    ),
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
        appears_when = self._selectors[page_name]['appears when']
        if isinstance(appears_when, dict):
            if "attribute" in appears_when.keys():
                key, value = appears_when["attribute"].split("=")
                return (By.XPATH, "(//*[@{0}='{1}'])[1]".format(key, value))
        else:
            seltype, ident = appears_when.split("=")
            return (By.CSS_SELECTOR, "#{0}".format(ident))

    def the(self, name):
        element_yaml = self._selectors[self._current_page]['elements'][name]
        if isinstance(element_yaml, dict):
            if "attribute" in element_yaml.keys():
                key, value = element_yaml["attribute"].split("=")
                return WebElement(self, "xpath", "(//*[@{0}='{1}'])[1]".format(key, value))
            if "xpath" in element_yaml.keys():
                return WebElement(self, "xpath", element_yaml['xpath'])
        else:
            seltype, ident = element_yaml.split("=")
            return WebElement(self, seltype, ident)
