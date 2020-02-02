#!/usr/bin/env python3

import datetime
import sys
from subprocess import PIPE, Popen

import pypandoc
import requests
from bs4 import BeautifulSoup

NUM_CHAPTERS = 122


def main():
    for chapter in range(1, NUM_CHAPTERS + 1):
        write_man_page_chapter(chapter)


def scrape_chapter(chapter_num):
    url = f"https://www.hpmor.com/chapter/{chapter_num}"
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
    proc = Popen(["go-md2man"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
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

    return f", __{man_page_name(chapter_num + 1)}__(7)"


def add_header(chapter_num, title, markdown):
    name = man_page_name(chapter_num).upper()
    date = datetime.date.today().isoformat()
    next_chap = next_chapter_string(chapter_num)
    return (
        # fields: title section date source manual
        f'{name} 7 "{date}" "Eliezer Yudkowsky" "HPMOR"\n'
        "==============================================\n"
        "# NAME\n"
        f"{title}\n"
        "# DESCRIPTION\n"
        f"{markdown}\n"
        "# SEE ALSO\n"
        f"__hpmor-man-pages__(7){next_chap}\n")


def make_man_page_chapter(chapter_num):
    (title, html) = scrape_chapter(chapter_num)
    markdown = pypandoc.convert_text(html, to="markdown_strict", format="html")
    markdown = add_header(chapter_num, title, markdown)
    man_page = md2man(markdown)
    return man_page


def man_page_name(chapter_num):
    num_str = str(chapter_num).zfill(3)
    return f"hpmor-{num_str}"


def write_man_page_chapter(chapter_num):
    man_page = make_man_page_chapter(chapter_num)
    name = man_page_name(chapter_num)
    path = f"out/{name}.7"
    with open(path, "w") as file:
        file.write(man_page)


if __name__ == "__main__":
    main()
