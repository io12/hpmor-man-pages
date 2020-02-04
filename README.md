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

If you don't want to install the man pages, you can open them locally with `man -l ./man7/hpmor-001.7`.

### Arch Linux

Arch Linux users can install [`hpmor-man-pages-git`](https://aur.archlinux.org/packages/hpmor-man-pages-git/) from the AUR.

## Usage

```
man hpmor-man-pages     # table of contents
man hpmor-001           # chapter 1
```
