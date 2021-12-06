run_pylint:
	@echo "Running pylint"
	python3 -m pylint aoc

run_pytest:
	@echo "Running pytest"
	python3 -m pytest -v -s test

run_format:
	@echo "Running isort and black"
	isort --profile black aoc && black aoc

stub_day:
	if [ -z "$(DAY)" ]; then echo "Must input a DAY=X parameter!" && exit 125; fi
	@echo "Making day $(DAY)"
	@$(eval DAY_FILE := aoc/y2021/day$(DAY).py)
	@$(eval TEST_DAY_FILE := test/test_day$(DAY).py)
	@cp -n aoc/y2021/day0.py $(DAY_FILE)
	@sed -i s/Day\ 0/Day\ $(DAY)/g $(DAY_FILE)
	@sed -i s/day0/day$(DAY)/g $(DAY_FILE)
	@sed -i s/TEST_ANSWER/`cat inputs/test_day$(DAY)_answer.txt`/g $(DAY_FILE)
	@cp -n test/test_day0.py $(TEST_DAY_FILE)
	@sed -i s/Day\ 0/Day\ $(DAY)/g $(TEST_DAY_FILE)
	@sed -i s/day0/day$(DAY)/g $(TEST_DAY_FILE)
	@python -m aoc.y2021.get_test $(DAY)
	@curl \
		-X GET \
		-H "Cookie: session=${AOC_SESSION}" \
		-o "inputs/day${DAY}.txt" \
		"https://adventofcode.com/2021/day/${DAY}/input"
	# just use VScode so no need to open vim
	# @gnome-terminal -x bash -ic "vi $(DAY_FILE); bash" &
	@if grep -q day$(DAY) setup.cfg; then echo exists; \
		else echo "  run_day$(DAY) = aoc.y2021.day$(DAY):main" >> setup.cfg && \
		pip install --no-deps -e .; fi
	@run_day$(DAY)

precommit: run_format run_pylint run_pytest
