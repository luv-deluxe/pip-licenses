"""Small tool printing Python packages licenses from provided requirement file"""

from os import getenv as os_getenv
import re
import sys

import prettytable
from prettytable.colortable import ColorTable, Themes, Theme
import grequests

THEME = Theme(horizontal_color="93", vertical_color="93")
HEADERS = ["PACKAGE", "VERSION", "LICENSE"]
PROXIES = {
    "http": os_getenv("HTTP_PROXY", ""),
    "https": os_getenv("HTTP_PROXY", ""),
}


def get_reqs_urls() -> list:
    pattern = re.compile(r"^(.+)[><=]{2}(.+)$", re.IGNORECASE)
    pattern_nolock = re.compile(r"(^.+)[^><=]{2}(.+)&", re.IGNORECASE)
    requirements = []
    try:
        reqs_file = sys.argv[1]
    except IndexError:
        raise SystemExit("Missing requirement file")
    with open(reqs_file, "r", encoding="utf-8") as reqs:
        requirements = reqs.read().splitlines()
    if not requirements:
        raise SystemExit(f"No requirements in {reqs_file}")

    # return [pattern.findall(req)[0] for req in requirements]
    return list(map(lambda x: pattern.findall(x)[0], requirements))


def compile_url(pkg: tuple):
    return f"https://pypi.org/project/{pkg[0]}/{pkg[1]}/"


def retrieve_license(html_body: str) -> tuple[str, str, str]:
    pattern_lic = re.compile(r"<strong>License:.+>(.+)<")
    pattern_namever = re.compile(r"<h1 class=\"package-header__name\">\n{0,1}(.+)\n{0,1}.+</h1>")
    license: str = pattern_lic.findall(html_body)[1].strip()
    name, version = pattern_namever.findall(html_body)[0].strip().split()
    return name, version, license


def main():
    req_gets = map(lambda x: grequests.get(compile_url(x), proxies=PROXIES), get_reqs_urls())
    results = grequests.map(req_gets)

    table = ColorTable(field_names=HEADERS, theme=THEME)
    table.align.update({col: "l" for col in HEADERS})

    # for req_info in get_reqs_urls():
    #     resp = requests.get(compile_url(req_info), proxies=PROXIES)
    #     pattern = re.compile(r"<strong>License:.+>(.+)<")
    #     license: str = pattern.findall(resp.text)[1].strip()
    #     table.add_row([req_info[0], req_info[1], license])
    # print(table)
    table.add_rows(list(map(lambda x: retrieve_license(x.text), results)))
    print(table.get_string(sortby="LICENSE"))
    with open("python-pkgs-license.html", "w", encoding="utf-8") as htmltable:
        htmltable.write(
            table.get_html_string(
                title="Python Packages licesnes",
                format=True,
                border=True,
                sortby="LICENSE",
                vrules=prettytable.NONE,
                hrules=prettytable.ALL,
            )
        )

    with open("python-pkgs-license.csv", "w", encoding="utf-8") as csvtable:
        csvtable.write(table.get_csv_string().replace("\r\n", "\n").replace(",", "; "))
