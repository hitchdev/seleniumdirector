from strictyaml import load, MapPattern, Optional, Enum, Str, Map, Int, Any
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


ELEMENTS_SCHEMA = MapPattern(
    Str(),
    Str()
    | Map(
        {
            Optional("in iframe"): Str(),
            Optional("which"): Enum(["last"]) | Int(),
            Optional("but parent"): Int(),
            Optional("subelements"): Any(),
            # SELECTORS
            Optional("id"): Str(),
            Optional("class"): Str(),
            Optional("attribute"): Str(),
            Optional("text is"): Str(),
            Optional("text contains"): Str(),
            Optional("xpath"): Str(),
        }
    ),
)


def revalidate_subelements(elements):
    for name, options in elements.items():
        if "subelements" in options:
            options["subelements"].revalidate(ELEMENTS_SCHEMA)
            revalidate_subelements(options["subelements"])


def parse_yaml(yaml_text):
    selectors = load(
        yaml_text,
        MapPattern(Str(), Map({"appears when": Str(), "elements": ELEMENTS_SCHEMA})),
    )

    for page, page_properties in selectors.items():
        revalidate_subelements(page_properties["elements"])
    return selectors


class ElementData(object):
    def __init__(self, name, page, element_yaml):
        self._name = name
        self._page = page
        self._element_yaml = element_yaml

    @property
    def names(self):
        return [name.strip() for name in self._name.split("/")]

    @property
    def first_yaml(self):
        return self.yaml_items[0]

    @property
    def yaml_items(self):
        def yaml_from(names, element_yaml):
            if len(names) == 1:
                return element_yaml[names[0].strip()]
            else:
                return yaml_from(
                    names[1:], element_yaml[names[0].strip()]["subelements"]
                )

        items = []

        for i in range(1, len(self.names) + 1):
            try:
                items.append(
                    yaml_from(self.names[:i], self._element_yaml["elements"]).data
                )
            except KeyError:
                raise exceptions.NotFoundInSelectors(
                    "'{}' not found in selectors file for page '{}'.".format(
                        self._name, self._page
                    )
                )

        return items

    @property
    def xpath(self):
        full_path = u""

        for yaml_item in self.yaml_items:
            for selector_type in DEFAULT_SELECTORS.keys():
                if selector_type in yaml_item.keys():
                    path = DEFAULT_SELECTORS[selector_type](yaml_item)

                    if "but parent" in yaml_item.keys():
                        path = "{}{}".format(path, "/.." * yaml_item["but parent"])

                    if "which" in yaml_item.keys():
                        path = "({})[{}]".format(
                            path,
                            yaml_item["which"]
                            if yaml_item["which"] != "last"
                            else "last()",
                        )

                    full_path += path

        return full_path


class WebDirector(object):
    def __init__(self, driver, selector_file, fake_time=None, default_timeout=5):
        self.driver = driver
        self._selectors = parse_yaml(Path(selector_file).text())
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
        element_data = ElementData(name, page, self._selectors[page])

        if isinstance(element_data.first_yaml, dict):
            return WebElement(
                self,
                name,
                page,
                element_data.xpath,
                iframe_container=(
                    self._select(element_data.first_yaml["in iframe"], page)
                    if "in iframe" in element_data.first_yaml.keys()
                    else None
                ),
            )
        else:
            seltype, ident = element_data.first_yaml.split("=")
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
