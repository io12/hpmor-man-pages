.POSIX:

PREFIX = /usr/local

MAN_DIR = $(DESTDIR)$(PREFIX)/man/man7
OUT_DIR = man7
MAN_GLOB = hpmor-*.7
VENV_PATH = venv
VENV_ACTIVATE = $(VENV_PATH)/bin/activate
VENV_CMD = . $(VENV_ACTIVATE) &&
PYTHON = python3
PIP = pip3

.PHONY: all clean install uninstall

all: $(VENV_ACTIVATE)
	$(VENV_CMD) ./hpmor_man_pages.py

$(VENV_ACTIVATE): requirements.txt
	$(PYTHON) -m venv $(VENV_PATH)
	$(VENV_CMD) $(PIP) install -r $<

clean:
	rm -rf __pycache__ $(VENV_PATH) $(OUT_DIR)/$(MAN_GLOB)

install:
	mkdir -p $(MAN_DIR)
	cp $(OUT_DIR)/$(MAN_GLOB) $(MAN_DIR)

uninstall:
	rm -f $(MAN_DIR)/$(MAN_GLOB)
