install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
	#force install latest whisper
	pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
#test:
#	python -m pytest -vv --cov=main --cov=mylib --cov=funcLog --cov=gcpFunc test_*.py

format:	
	black *.py ec2-auto-scaling/*.py

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py ec2-auto-scaling/*.py

#container-lint:
#	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

all: install lint format