from seleniumdirector.webelement import WebElement
from selenium.webdriver import Chrome
from strictyaml import load, MapPattern, Optional, Enum, Str, Map, Int
from path import Path
import json


THIS_DIRECTORY = Path(__file__).realpath().dirname()


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
                            | Map({"class": Str(), Optional("which"): Enum(["last"]) | Int()})
                            | Map({"attribute": Str()})
                            | Map({"xpath": Str()})
                            | Map({
                                "text contains": Str(),
                                Optional("which"): Enum(["last"]) | Int()
                            })
                            | Map({"text is": Str()}),
                        ),
                    }
                ),
            ),
        ).data
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
        appears_when = self._selectors[page_name]["appears when"]
        self._select(appears_when, page_name).should_be_on_page()
        self._current_page = page_name

    def _select(self, name, page):
        element_yaml = self._selectors[page]["elements"][name]
        if isinstance(element_yaml, dict):
            if "class" in element_yaml.keys():
                if "which" in element_yaml.keys():
                    return WebElement(
                        self,
                        "xpath",
                        (
                            "(//*[contains("
                            "concat(' ', normalize-space(@class), ' '), "
                            "' {} ')])[{}]"
                        ).format(
                            element_yaml["class"],
                            element_yaml['which'] if element_yaml['which'] != "last" else "last()"
                        ),
                    )
                else:
                    return WebElement(
                        self,
                        "xpath",
                        (
                            "//*[contains("
                            "concat(' ', normalize-space(@class), ' '), "
                            "' {} ')]"
                        ).format(element_yaml["class"]),
                    )
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
                xpath = '//*[contains(text(), "{}")]'.format(element_yaml["text contains"])
                if "which" in element_yaml.keys():
                    xpath = "({})[{}]".format(
                        xpath,
                        element_yaml['which'] if element_yaml['which'] != "last" else "last()"
                    )
                return WebElement(self, "xpath", xpath)
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
                raise Exception("seltype {} not recognized".format(ident))
            return WebElement(self, seltype, ident)

    def the(self, name):
        return self._select(name, self._current_page)
