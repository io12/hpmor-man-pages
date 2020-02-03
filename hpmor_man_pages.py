#!/usr/bin/env python3

import datetime
import sys
from subprocess import PIPE, Popen

import pypandoc
import requests
from bs4 import BeautifulSoup

HPMOR_CHAP_URL = "https://www.hpmor.com/chapter/"
TOC_NAME = "hpmor-man-pages"
NUM_CHAPTERS = 122


def main():
    write_toc()
    for chapter in range(1, NUM_CHAPTERS + 1):
        write_man_page_chapter(chapter)


def scrape_toc():
    url = f"{HPMOR_CHAP_URL}1"
    print("fetching chapter list")
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, features="lxml")
    chapters = soup.find("select").find_all("option")
    chapters = [chap.text for chap in chapters]
    chapters = filter(lambda chap: chap != "Home", chapters)
    chapters = [chap.split(sep=": ", maxsplit=1)[1] for chap in chapters]
    return chapters


def markdown_man_title_line(name):
    name = name.upper()
    date = datetime.date.today().isoformat()
    return (
        # fields: title section date source manual
        f'{name} 7 "{date}" "Eliezer Yudkowsky" "HPMOR"\n'
        "==============================================\n")


def make_markdown_toc(chapters):
    chapters = [
        f"| {man_page_link(i + 1)} | {chap} |"
        for (i, chap) in enumerate(chapters)
    ]
    chapters = "\n".join(chapters)
    chapters = ("| Man page | Name |\n"
                "|----------+------|\n"
                f"{chapters}\n")
    return (
        # fields: title section date source manual
        f"{markdown_man_title_line(TOC_NAME)}\n"
        "# NAME\n"
        "Harry Potter and the Methods of Rationality, Unix Man Page Edition\n"
        "# CHAPTERS\n"
        f"{chapters}\n"
        "# SEE ALSO\n"
        f"{man_page_link(1)}\n")


def scrape_chapter(chapter_num):
    url = f"{HPMOR_CHAP_URL}{chapter_num}"
    print(url)
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, features="lxml")
    title = soup.title.text
    chapter_html = soup.find(id="storycontent")

    # Replace <span> tags with <b>. In HPMOR, <span> is used for underlining,
    # but man pages don't support underlining.
    for span in chapter_html.find_all("span"):
        tag = soup.new_tag("b")
        tag.string = span.string
        span.replace_with(tag)

    chapter_html = "".join(map(str, chapter_html.children))
    return (title, chapter_html)


def md2man(markdown):
    proc = Popen(["go-md2man"],
                 stdin=PIPE,
                 stdout=PIPE,
                 stderr=PIPE,
                 text=True)
    (stdout, stderr) = proc.communicate(markdown)

    if stderr != "" or proc.returncode != 0:
        print("error running go-md2man:", proc.returncode, stderr)
        print("FAILED MARKDOWN BEGIN")
        print(markdown)
        print("FAILED MARKDOWN END")
        sys.exit(1)

    return stdout


def next_chapter_string(chapter_num):
    if chapter_num == NUM_CHAPTERS:
        return ""

    return f", {man_page_link(chapter_num + 1)}"


def add_chap_header(chapter_num, title, markdown):
    name = man_page_name(chapter_num)
    next_chap = next_chapter_string(chapter_num)
    return (f"{markdown_man_title_line(name)}\n"
            "# NAME\n"
            f"{title}\n"
            "# DESCRIPTION\n"
            f"{markdown}\n"
            "# SEE ALSO\n"
            f"__{TOC_NAME}__(7){next_chap}\n")


def make_man_page_chapter(chapter_num):
    (title, html) = scrape_chapter(chapter_num)
    markdown = pypandoc.convert_text(html, to="markdown_strict", format="html")
    markdown = add_chap_header(chapter_num, title, markdown)
    man_page = md2man(markdown)
    return man_page


def make_man_page_toc():
    chapters = scrape_toc()
    markdown = make_markdown_toc(chapters)
    man_page = md2man(markdown)
    return man_page


def man_page_name(chapter_num):
    num_str = str(chapter_num).zfill(3)
    return f"hpmor-{num_str}"


def man_page_link(chapter_num):
    return f"__{man_page_name(chapter_num)}__(7)"


def write_toc():
    man_page = make_man_page_toc()
    write_man_page(TOC_NAME, man_page)


def write_man_page_chapter(chapter_num):
    name = man_page_name(chapter_num)
    man_page = make_man_page_chapter(chapter_num)
    write_man_page(name, man_page)


def write_man_page(name, man_page):
    path = f"man7/{name}.7"
    with open(path, "w") as file:
        file.write(man_page)


if __name__ == "__main__":
    main()
