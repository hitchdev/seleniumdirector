from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from strictyaml import load, MapPattern, Str, Map
from selenium.webdriver.common.by import By
from seleniumdirector import exceptions
from path import Path
import json


THIS_DIRECTORY = Path(__file__).realpath().dirname()


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


class WebSelector(object):
    def __init__(self, driver, selector_file, fake_time=None):
        self.driver = driver
        self._selectors = load(
            Path(selector_file).text(),
            MapPattern(
                Str(),
                Map(
                    {
                        "appears when": Str(),
                        "elements": MapPattern(
                            Str(),
                            Str()
                            | Map({"attribute": Str()})
                            | Map({"xpath": Str()})
                            | Map({"text contains": Str()})
                            | Map({"text is": Str()}),
                        ),
                    }
                ),
            ),
        ).data
        self._current_page = None
        self.default_timeout = 5
        self._use_faketime = False
        self._faketime = None

        if fake_time is not None:
            assert isinstance(self.driver, Chrome)
            response = self.driver.command_executor._request(
                "POST",
                "{}/session/{}/chromium/send_command_and_get_result".format(
                    driver.command_executor._url, driver.session_id
                ),
                json.dumps(
                    {
                        "cmd": "Page.addScriptToEvaluateOnNewDocument",
                        "params": {
                            "source": "{}\n{}".format(
                                THIS_DIRECTORY.joinpath("timemachine.js").text(),
                                "timemachine.config({timestamp: "
                                + str(fake_time.timestamp() * 1000)
                                + "});",
                            )
                        },
                    }
                ),
            )
            assert response["status"] == 0, "Error faking time {}".format(str(response))

    def visit(self, url):
        self.driver.get(url)

    def wait_for_page(self, page_name):
        appears_when = self._selectors[page_name]["appears when"]
        self._select(appears_when, page_name).should_appear()
        self._current_page = page_name

    def _select(self, name, page):
        element_yaml = self._selectors[page]["elements"][name]
        if isinstance(element_yaml, dict):
            if "attribute" in element_yaml.keys():
                key, value = element_yaml["attribute"].split("=")
                return WebElement(
                    self, "xpath", "(//*[@{0}='{1}'])[1]".format(key, value)
                )
            if "xpath" in element_yaml.keys():
                return WebElement(self, "xpath", element_yaml["xpath"])
            if "text is" in element_yaml.keys():
                return WebElement(
                    self,
                    "xpath",
                    '(//*[text()="{}"])[1]'.format(element_yaml["text is"]),
                )
            if "text contains" in element_yaml.keys():
                return WebElement(
                    self,
                    "xpath",
                    '(//*[contains(text(), "{}")])[1]'.format(
                        element_yaml["text contains"]
                    ),
                )
        else:
            seltype, ident = element_yaml.split("=")
            if seltype == "id":
                seltype = "xpath"
                ident = "//*[@id='{0}']".format(ident)
            elif seltype == "class":
                seltype = "xpath"
                ident = (
                    "//*[contains("
                    "concat(' ', normalize-space(@class), ' '), "
                    "' {} ')]"
                ).format(ident)
            else:
                raise Exception("seltype {} not recognized")
            return WebElement(self, seltype, ident)

    def the(self, name):
        return self._select(name, self._current_page)
