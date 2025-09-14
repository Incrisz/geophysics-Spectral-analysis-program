# Geophysics Spectral Analysis Program

Interactive Streamlit application for exploring geophysical data through interpolation, regression, and spectral analysis.

## Features
- Upload Excel (`.xlsx`) or text (`.txt`) files containing depth and resistivity data.
- Plotly-powered charts for interactive data, regression, and spectral views.
- Sample datasets are available in the `dataset/` folder.

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Incrisz/geophysics-Spectral-analysis-program.git
cd geophysics-Spectral-analysis-program
```

### 2. Create a virtual environment
**Windows**
```bash
python -m venv venv
venv\\Scripts\\activate
```
**macOS/Linux**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run upgrade.py
```
Open the URL displayed in the terminal to interact with the application.

## Makefile commands
Use the provided `Makefile` to simplify common tasks:
```bash
make install      # install dependencies
make run          # start the Streamlit app
make docker-build # build the Docker image
make docker-run   # run the app in a container
```

## Docker
To build and run the app using Docker directly:
```bash
docker build -t spectral-app .
docker run -p 8501:8501 spectral-app
```

## Docker Compose
To build and run the app using Docker Compose:
```bash
docker compose up --build
```
This will expose the app on http://localhost:8501.

