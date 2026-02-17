# Use the venv python directly (no activation needed)
PY = .venv/Scripts/python.exe

.PHONY: venv install test run-easy run-medium run-hard clean

venv:
	python -m venv .venv
	$(PY) -m pip install -U pip

install: venv
	$(PY) -m pip install -U pip
	$(PY) -m pip install pytest
	$(PY) -m pip install -e .

test: install
	$(PY) -m pytest -q

run-easy: install
	$(PY) -m marry_me.simulation_async data/events_easy.json

run-medium: install
	$(PY) -m marry_me.simulation_async data/events_medium.json

run-hard: install
	$(PY) -m marry_me.simulation_async data/events_hard.json

clean:
	$(PY) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"