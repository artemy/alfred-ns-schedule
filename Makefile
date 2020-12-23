PYTHON=python2
PIP=pip
NS_SCHEDULE_PY=ns_schedule.py
NS_SCHEDULE_TEST_PY=ns_schedule_test.py
ALFRED_FILE_NAME=NS_Schedule
ALFRED_PACKAGE_FILES=./alfred/*

.PHONY: clean test build

all: clean test build

clean:
	rm -fr out *.alfredworkflow

test:
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PYTHON) $(NS_SCHEDULE_TEST_PY)

build:
	zip -j -r $(ALFRED_FILE_NAME).alfredworkflow $(ALFRED_PACKAGE_FILES) $(NS_SCHEDULE_PY)