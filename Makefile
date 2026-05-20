.PHONY: setup generate train evaluate test lint run docker-build docker-run smoke clean tf-fmt

setup:
	python -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

generate:
	python training/data_generator.py

train:
	python training/train.py

evaluate:
	python training/evaluate.py

test:
	pytest -q

lint:
	ruff check .

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t pharma-mlops-clinical-risk-api:local .

docker-run:
	docker run --rm -p 8000:8000 --env-file .env.example pharma-mlops-clinical-risk-api:local

smoke:
	bash scripts/smoke_test.sh

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ app/__pycache__ training/__pycache__

tf-fmt:
	cd infra/terraform && terraform fmt
