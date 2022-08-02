NS_SCHEDULE_PY=ns_schedule.py
ALFRED_FILE_NAME=NS_Schedule
ALFRED_PACKAGE_FILES=./alfred/* .readme/images/screenshot.png

.PHONY: clean test build

all: clean build

clean:
	rm -fr out *.alfred5workflow

build:
	zip -j -r $(ALFRED_FILE_NAME).alfred5workflow $(ALFRED_PACKAGE_FILES) $(NS_SCHEDULE_PY)
