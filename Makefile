.POSIX:

PREFIX = /usr/local

MAN_DIR = $(DESTDIR)$(PREFIX)/man/man7
OUT_DIR = man7
MAN_GLOB = hpmor-*.7

.PHONY: all clean install uninstall

all:
	./hpmor_man_pages.py

clean:
	rm -rf __pycache__ $(OUT_DIR)/$(MAN_GLOB)

install:
	mkdir -p $(MAN_DIR)
	cp $(OUT_DIR)/$(MAN_GLOB) $(MAN_DIR)

uninstall:
	rm -f $(MAN_DIR)/$(MAN_GLOB)
