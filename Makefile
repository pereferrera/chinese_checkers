# no buildin rules and variables
MAKEFLAGS =+ -rR --warn-undefined-variables

IMAGE_BASE_NAME = ferrerabertran/chinese_checkers
IMAGE_TAG = $(shell git describe --tags --always --dirty)

create_env:
	python3.7 -m venv venv --without-pip --system-site-packages
	. venv/bin/activate && python3 -m pip install -r requirements.txt

run:
	. venv/bin/activate && python3 -m chinese_checkers.play

test:
	. venv/bin/activate && nosetests --with-coverage \
	   --cover-package=chinese_checkers \
       --cover-min-percentage=75 \
       tests
    
lint:
	. venv/bin/activate && flake8 chinese_checkers/

static-typing:
	. venv/bin/activate && mypy chinese_checkers/

