#!/usr/bin/env python3

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
    chapter_html = soup.find(id="storycontent")
    chapter_html = "".join(map(str, chapter_html.children))
    return chapter_html


def md2man(markdown):
    proc = Popen(["go-md2man"], stdin=PIPE, stdout=PIPE, text=True)
    (stdout, stderr) = proc.communicate(markdown)

    if stderr is not None or proc.returncode != 0:
        print("error running go-md2man:", proc.returncode, stderr)
        sys.exit(1)

    return stdout


def make_man_page_chapter(chapter_num):
    html = scrape_chapter(chapter_num)
    markdown = pypandoc.convert_text(html, to="markdown-smart", format="html")
    man_page = md2man(markdown)
    return man_page


def write_man_page_chapter(chapter_num):
    man_page = make_man_page_chapter(chapter_num)
    num_str = str(chapter_num).zfill(3)
    path = f"out/hpmor-{num_str}.7"
    with open(path, "w") as file:
        file.write(man_page)


if __name__ == "__main__":
    main()
