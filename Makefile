.PHONY: install run docker-build docker-run

install:
	pip install -r requirements.txt

run:
	streamlit run upgrade.py

docker-build:
	docker build -t spectral-app .

docker-run:
	docker run -p 8501:8501 spectral-app
