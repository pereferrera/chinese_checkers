# no buildin rules and variables
MAKEFLAGS =+ -rR --warn-undefined-variables

create_env:
	python3 -m venv venv --without-pip --system-site-packages
	. venv/bin/activate && python3 -m pip install -r requirements.txt

run:
	. venv/bin/activate && python3 -m chinese_checkers.play

test:
	. venv/bin/activate && python3 -m "nose" --with-coverage --cover-package=chinese_checkers tests
    
lint:
	. venv/bin/activate && flake8 chinese_checkers/ --extend-ignore=RST212,RST201,RST301,RST203


