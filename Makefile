NS_SCHEDULE_PY=ns_schedule.py
ALFRED_FILE_NAME=NS_Schedule
ALFRED_PACKAGE_FILES=./alfred/*

.PHONY: clean test build

all: clean build

clean:
	rm -fr out *.alfredworkflow

build:
	zip -j -r $(ALFRED_FILE_NAME).alfredworkflow $(ALFRED_PACKAGE_FILES) $(NS_SCHEDULE_PY)