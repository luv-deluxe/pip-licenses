from codecs import open
from os import path

from setuptools import setup

from piplic import __author__ as AUTHOR
from piplic import __version__ as VERSION
from piplic import __doc__ as DESCRIPTION

here = path.abspath(path.dirname(__file__))


def read_file(filename):
    content = ""
    with open(path.join(here, filename), encoding="utf-8") as f:
        content = f.read()

    return content


LONG_DESC = read_file("README.md")
LICENSE = read_file("LICENSE")
REQUIREMENTS = read_file("requirements.txt").split()
print(REQUIREMENTS)
setup(
    name="piplic",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    url="https://github.com/luv-deluxe/piplic",
    author=AUTHOR,
    license=LICENSE,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "piplic=piplic:main",
        ],
    },
)
