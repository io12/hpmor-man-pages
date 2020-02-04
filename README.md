# `hpmor-man-pages`

Harry Potter and the Methods of Rationality, Unix Man Page Edition

## About

This repo contains scripts for building Unix man pages of Eliezer Yudkowsky's epic fanfic, [HPMOR](https://www.hpmor.com/).

![screenshot](https://i.imgur.com/xKx2Gx2.png)

## Installing

First, install the following build dependencies:
* `python3`
* `pandoc`
* `go-md2man`

Then run `make` to build the man pages and `sudo make install` to install them. To uninstall, run `sudo make uninstall`.

## Usage

```
man hpmor-man-pages     # table of contents
man hpmor-001           # chapter 1
```
