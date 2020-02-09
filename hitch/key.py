from hitchstory import StoryCollection, BaseEngine, HitchStoryException
from hitchstory import validate, no_stacktrace_for
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from hitchrun import expected
from icommandlib import ICommand, ICommandError
from commandlib import Command, CommandError, python, python_bin
from strictyaml import Str, Map, MapPattern, Bool, Enum, Optional, load
from pathquery import pathquery
from hitchrun import hitch_maintenance
from hitchrun import DIR
from hitchrun.decorators import ignore_ctrlc
from hitchrunpy import (
    ExamplePythonCode,
    HitchRunPyException,
    ExpectedExceptionMessageWasDifferent,
)
import requests
from path import Path
import hitchbuildpy
import dirtemplate
import signal


def project_build(paths, python_version, selenium_version=None):
    pylibrary = (
        hitchbuildpy.PyLibrary(
            name="py{0}".format(python_version),
            base_python=hitchbuildpy.PyenvBuild(python_version).with_build_path(
                paths.share
            ),
            module_name="seleniumdirector",
            library_src=paths.project,
        )
        .with_requirementstxt(paths.key / "debugrequirements.txt")
        .with_build_path(paths.gen)
    )

    if selenium_version is not None:
        pylibrary = pylibrary.with_packages("selenium=={0}".format(selenium_version))

    pylibrary.ensure_built()
    return pylibrary


class Engine(BaseEngine):
    """Python engine for running tests."""
    given_definition = GivenDefinition(
        python_version=GivenProperty(Str()),
        selenium_version=GivenProperty(Str()),
        website=GivenProperty(MapPattern(Str(), Str())),
        selectors_yml=GivenProperty(Str()),
        javascript=GivenProperty(Str()),
        setup=GivenProperty(Str()),
        code=GivenProperty(Str()),
    )

    info_definition = InfoDefinition(
        status=InfoProperty(schema=Enum(["experimental", "stable"])),
        docs=InfoProperty(schema=Str()),
    )


    def __init__(self, keypath, settings):
        self.path = keypath
        self.settings = settings

    def set_up(self):
        """Set up your applications and the test environment."""
        self.path.state = self.path.gen.joinpath("state")
        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        self.path.profile = self.path.gen.joinpath("profile")
        dirtemplate.DirTemplate(
            "webapp", self.path.key / "htmltemplate", self.path.state
        ).with_vars(javascript=self.given.get("javascript", "")).with_files(
            base_html={
                filename: {"content": content}
                for filename, content in self.given.get("website", {}).items()
            }
        ).ensure_built()

        self.path.state.joinpath("selectors.yml").write_text(
            self.given["selectors.yml"]
        )

        self.server = (
            python("-m", "http.server").in_dir(self.path.state / "webapp").pexpect()
        )
        self.server.expect("Serving HTTP on 0.0.0.0")

        if not self.path.profile.exists():
            self.path.profile.mkdir()

        self.python = project_build(
            self.path, self.given["python version"], self.given["selenium version"]
        ).bin.python

        self.example_py_code = (
            ExamplePythonCode(self.python, self.path.state)
            .with_setup_code(self.given.get("setup", ""))
            .with_terminal_size(160, 100)
            .with_long_strings()
        )

    @validate(
        code=Str(),
        will_output=Map({"in python 2": Str(), "in python 3": Str()}) | Str(),
        raises=Map(
            {
                Optional("type"): Map({"in python 2": Str(), "in python 3": Str()})
                | Str(),
                Optional("message"): Map({"in python 2": Str(), "in python 3": Str()})
                | Str(),
            }
        ),
        in_interpreter=Bool(),
    )
    def run(self, code, will_output=None, raises=None, in_interpreter=False):
        if in_interpreter:
            code = "{0}\nprint(repr({1}))".format(
                "\n".join(code.strip().split("\n")[:-1]), code.strip().split("\n")[-1]
            )

        to_run = self.example_py_code.with_code(code)

        if self.settings.get("cprofile"):
            to_run = to_run.with_cprofile(
                self.path.profile.joinpath("{0}.dat".format(self.story.slug))
            )

        result = (
            to_run.expect_exceptions().run() if raises is not None else to_run.run()
        )

        if will_output is not None:
            actual_output = "\n".join(
                [line.rstrip() for line in result.output.split("\n")]
            )
            try:
                Templex(will_output).assert_match(actual_output)
            except NonMatching:
                if self.settings.get("rewrite"):
                    self.current_step.update(**{"will output": actual_output})
                else:
                    raise

        if raises is not None:
            differential = False  # Difference between python 2 and python 3 output?
            exception_type = raises.get("type")
            message = raises.get("message")

            if exception_type is not None:
                if not isinstance(exception_type, str):
                    differential = True
                    exception_type = (
                        exception_type["in python 2"]
                        if self.given["python version"].startswith("2")
                        else exception_type["in python 3"]
                    )

            if message is not None:
                if not isinstance(message, str):
                    differential = True
                    message = (
                        message["in python 2"]
                        if self.given["python version"].startswith("2")
                        else message["in python 3"]
                    )

            try:
                result.exception_was_raised(exception_type, message)
            except ExpectedExceptionMessageWasDifferent as error:
                if self.settings.get("rewrite") and not differential:
                    new_raises = raises.copy()
                    new_raises["message"] = result.exception.message
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def do_nothing(self):
        pass

    def pause(self, message="Pause"):
        import IPython

        IPython.embed()

    def tear_down(self):
        self.server.kill(signal.SIGTERM)
        self.server.wait()


def _storybook(settings):
    return StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR, settings))


def _current_version():
    return DIR.project.joinpath("VERSION").bytes().decode("utf8").rstrip()


def _personal_settings():
    settings_file = DIR.key.joinpath("personalsettings.yml")

    if not settings_file.exists():
        settings_file.write_text(
            (
                "engine:\n"
                "  rewrite: no\n"
                "  cprofile: no\n"
                "params:\n"
                "  python version: 3.5.0\n"
            )
        )
    return load(
        settings_file.bytes().decode("utf8"),
        Map(
            {
                "engine": Map({"rewrite": Bool(), "cprofile": Bool()}),
                "params": Map({"python version": Str()}),
            }
        ),
    )


@expected(HitchStoryException)
def bdd(*keywords):
    """
    Run stories matching keywords.
    """
    settings = _personal_settings().data
    _storybook(settings["engine"]).with_params(
        **{"python version": settings["params"]["python version"]}
    ).only_uninherited().shortcut(*keywords).play()


@expected(HitchStoryException)
def rbdd(*keywords):
    """
    Run stories matching keywords.
    """
    settings = _personal_settings().data
    settings["rewrite"] = True
    _storybook(settings["engine"]).with_params(
        **{"python version": settings["params"]["python version"]}
    ).only_uninherited().shortcut(*keywords).play()


@expected(HitchStoryException)
def regressfile(filename):
    """
    Run all stories in filename 'filename' in python 2 and 3.

    Rewrite stories if appropriate.
    """
    _storybook({"rewrite": False}).in_filename(filename).with_params(
        **{"python version": "2.7.10"}
    ).filter(lambda story: not story.info["fails on python 2"]).ordered_by_name().play()

    _storybook({"rewrite": False}).with_params(
        **{"python version": "3.5.0"}
    ).in_filename(filename).ordered_by_name().play()


@expected(HitchStoryException)
def regression():
    """
    Run regression testing - lint and then run all tests.
    """
    lint()
    storybook = _storybook({}).only_uninherited()
    storybook.with_params(**{"python version": "3.5.0"}).ordered_by_name().play()


def lint():
    """
    Lint all code.
    """
    python("-m", "flake8")(
        DIR.project.joinpath("seleniumdirector"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    """
    python("-m", "flake8")(
        DIR.key.joinpath("key.py"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    """
    print("Lint success!")


def hitch(*args):
    """
    Use 'h hitch --help' to get help on these commands.
    """
    hitch_maintenance(*args)


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    NAME = "seleniumdirector"
    git = Command("git").in_dir(DIR.project)
    version_file = DIR.project.joinpath("VERSION")
    old_version = version_file.bytes().decode("utf8")
    if version_file.bytes().decode("utf8") != version:
        DIR.project.joinpath("VERSION").write_text(version)
        git("add", "VERSION").run()
        git(
            "commit", "-m", "RELEASE: Version {0} -> {1}".format(old_version, version)
        ).run()
        git("push").run()
        git("tag", "-a", version, "-m", "Version {0}".format(version)).run()
        git("push", "origin", version).run()
    else:
        git("push").run()

    # Set __version__ variable in __init__.py, build sdist and put it back
    initpy = DIR.project.joinpath(NAME, "__init__.py")
    original_initpy_contents = initpy.bytes().decode("utf8")
    initpy.write_text(original_initpy_contents.replace("DEVELOPMENT_VERSION", version))
    python("setup.py", "sdist").in_dir(DIR.project).run()
    initpy.write_text(original_initpy_contents)

    # Upload to pypi
    python("-m", "twine", "upload", "dist/{0}-{1}.tar.gz".format(NAME, version)).in_dir(
        DIR.project
    ).run()


@expected(dirtemplate.exceptions.DirTemplateException)
def docgen():
    """
    Build documentation.
    """

    def title(dirfile):
        assert len(dirfile.text().split("---")) >= 3, "{} doesn't have ---".format(
            dirfile
        )
        return load(dirfile.text().split("---")[1]).data.get("title", "misc")

    docfolder = DIR.gen / "docs"

    if docfolder.exists():
        docfolder.rmtree(ignore_errors=True)
    docfolder.mkdir()

    template = (
        dirtemplate.DirTemplate("docs", DIR.project / "docs", DIR.gen)
        .with_files(
            template_story_jinja2={
                "using/alpha/{0}.md".format(story.info["docs"]): {"story": story}
                for story in _storybook({}).ordered_by_name()
                if "docs" in story.info
            }
        )
        .with_vars(
            include_title=True,
            readme=False,
            quickstart=_storybook({})
            .in_filename(DIR.key / "html-ids.story")
            .non_variations()
            .ordered_by_file(),
        )
        .with_functions(title=title)
    )
    template.ensure_built()
    print("Docs generated")


@expected(CommandError)
def doctests():
    pylibrary = project_build(DIR, "2.7.10")
    pylibrary.bin.python(
        "-m", "doctest", "-v", DIR.project.joinpath("seleniumdirector", "utils.py")
    ).in_dir(DIR.project.joinpath("seleniumdirector")).run()

    pylibrary = project_build(DIR, "3.5.0")
    pylibrary.bin.python(
        "-m", "doctest", "-v", DIR.project.joinpath("seleniumdirector", "utils.py")
    ).in_dir(DIR.project.joinpath("seleniumdirector")).run()


@ignore_ctrlc
def ipy():
    """
    Run IPython in environment."
    """
    Command(DIR.gen.joinpath("py3.5.0", "bin", "ipython")).run()


def hvenvup(package, directory):
    """
    Install a new version of a package in the hitch venv.
    """
    pip = Command(DIR.gen.joinpath("hvenv", "bin", "pip"))
    pip("uninstall", package, "-y").run()
    pip("install", DIR.project.joinpath(directory).abspath()).run()


def black():
    """
    Reformat the code.
    """
    python_bin.black(DIR.project / "seleniumdirector").run()
    python_bin.black(DIR.key / "key.py").run()


def runserver():
    """
    Run web server.
    """
    python("-m", "http.server").in_dir(DIR.gen / "state" / "webapp").run()


def rerun(version="3.7.0"):
    """
    Rerun last example code block with specified version of python.
    """
    Command(DIR.gen.joinpath("py{0}".format(version), "bin", "python"))(
        DIR.gen.joinpath("state", "working", "examplepythoncode.py")
    ).in_dir(DIR.gen.joinpath("state", "working")).run()
