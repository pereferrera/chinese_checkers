# no buildin rules and variables
MAKEFLAGS =+ -rR --warn-undefined-variables

create_env:
	python3.7 -m venv venv --without-pip --system-site-packages
	. venv/bin/activate && python3.7 -m pip install -r requirements.txt

run:
	. venv/bin/activate && python3.7 -m chinese_checkers.play

test:
	. venv/bin/activate && python3.7 -m "nose" --with-coverage \
	--cover-package=chinese_checkers \
	--cover-min-percentage=75 \
	tests
    
lint:
	. venv/bin/activate && flake8 chinese_checkers/

static-typing:
	. venv/bin/activate && mypy chinese_checkers/ --ignore-missing-imports

