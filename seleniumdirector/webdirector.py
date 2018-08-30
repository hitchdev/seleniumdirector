from strictyaml import load, MapPattern, Optional, Enum, Str, Map, Int
from seleniumdirector.webelement import WebElement
from seleniumdirector import exceptions
from selenium.webdriver import Chrome
from path import Path
import json


THIS_DIRECTORY = Path(__file__).realpath().dirname()


def id_selector(element_yaml):
    return "//*[@id='{}']".format(element_yaml["id"])


def class_selector(element_yaml):
    return "//*[contains(concat(' ', normalize-space(@class), ' '), ' {} ')]".format(
        element_yaml["class"]
    )


def attribute_selector(element_yaml):
    key, value = element_yaml["attribute"].split("=")
    return "//*[@{0}='{1}']".format(key, value)


def text_is_selector(element_yaml):
    return '//*[text()="{}"]'.format(element_yaml["text is"])


def text_contains_selector(element_yaml):
    return '//*[contains(text(), "{}")]'.format(element_yaml["text contains"])


def xpath_selector(element_yaml):
    return element_yaml["xpath"]


DEFAULT_SELECTORS = {
    "id": id_selector,
    "class": class_selector,
    "attribute": attribute_selector,
    "text is": text_is_selector,
    "text contains": text_contains_selector,
    "xpath": xpath_selector,
}


class WebDirector(object):
    def __init__(self, driver, selector_file, fake_time=None, default_timeout=5):
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
                            | Map(
                                {
                                    Optional("in iframe"): Str(),
                                    Optional("which"): Enum(["last"]) | Int(),
                                    Optional("id"): Str(),
                                    Optional("class"): Str(),
                                    Optional("attribute"): Str(),
                                    Optional("xpath"): Str(),
                                    Optional("text contains"): Str(),
                                    Optional("text is"): Str(),
                                }
                            ),
                        ),
                    }
                ),
            ),
        )
        self._current_page = None
        self.default_timeout = default_timeout
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
        appears_when = self._selectors[page_name]["appears when"].data
        self._select(appears_when, page_name).should_be_on_page()
        self._current_page = page_name

    def _select(self, name, page):
        if name not in self._selectors[page]["elements"].data:
            raise exceptions.NotFoundInSelectors(
                "'{}' not found in selectors file for page '{}'.".format(name, page)
            )
        element_yaml = self._selectors[page]["elements"][name].data
        if isinstance(element_yaml, dict):
            for selector_type in DEFAULT_SELECTORS.keys():
                if selector_type in element_yaml.keys():
                    iframe_container = (
                        self._select(element_yaml["in iframe"], page)
                        if "in iframe" in element_yaml.keys()
                        else None
                    )

                    xpath = DEFAULT_SELECTORS[selector_type](element_yaml)
                    if "which" in element_yaml.keys():
                        xpath = "({})[{}]".format(
                            xpath,
                            element_yaml["which"]
                            if element_yaml["which"] != "last"
                            else "last()",
                        )
                    return WebElement(
                        self, name, page, xpath, iframe_container=iframe_container
                    )
            raise Exception("Selector not found")
        else:
            seltype, ident = element_yaml.split("=")
            if seltype == "id":
                return WebElement(self, name, page, "//*[@id='{0}']".format(ident))
            elif seltype == "class":
                return WebElement(
                    self,
                    name,
                    page,
                    (
                        "//*[contains("
                        "concat(' ', normalize-space(@class), ' '), "
                        "' {} ')]"
                    ).format(ident),
                )
            else:
                raise Exception("seltype {} not recognized".format(ident))

    def the(self, name):
        return self._select(name, self._current_page)
