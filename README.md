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
