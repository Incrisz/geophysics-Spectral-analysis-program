# Interactive Geophysical Spectral Analysis Tool

This repository contains a Python-based application for the spectral analysis of geophysical data. The tool provides an interactive interface for visualizing various data formats (including `.grd` and `.xlsx`) and performing spectral analysis to aid in geophysical interpretation.

## Features

-   **Multi-format Data Support:** Upload and process data from various file types, including `.grd`, `.xlsx`, `.segy`, and more.
-   **Interactive Plotting:** Visualize your data as heatmaps and interactively draw lines to calculate slope and intercept.
-   **Web-based Interface:** A user-friendly interface built with Streamlit.
-   **Customizable Analysis:** Adjust parameters for spectral analysis and grid map visualization.

## Setup and Installation

Follow these steps to set up and run the application on your local machine.

### Prerequisites

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/downloads/)

### Installation Steps

1.  **Clone the Repository:**
    Open your terminal or command prompt and run the following command:
    ```bash
    git clone https://github.com/Incrisz/geophysics-Spectral-analysis-program.git
    cd geophysics-Spectral-analysis-program
    ```

2.  **Create a Virtual Environment:**
    It is highly recommended to use a virtual environment to manage project dependencies.

    -   **On Windows:**
        ```bash
        python -m venv venv
        venv\\Scripts\\activate
        ```
    -   **On macOS and Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    This project uses a `requirements.txt` file to manage its dependencies. Install them with pip:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Once you have installed the dependencies, you can run the application using Streamlit:

```bash
streamlit run upgrade.py
```

This will start the application, and you can access it in your web browser at the local URL provided in the terminal (usually `http://localhost:8501`).

To make the app accessible from other devices on your network, run:
```bash
streamlit run upgrade.py --server.address=0.0.0.0 --server.port=8501
```
