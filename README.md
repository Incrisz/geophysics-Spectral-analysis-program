# Geophysics Spectral Analysis Program

This repository contains spectral analysis scripts for geophysical data interpretation using Python.

## Repository

[https://github.com/Incrisz/geophysics-Spectral-analysis-program.git](https://github.com/Incrisz/geophysics-Spectral-analysis-program.git)

## Setup Guide

Follow the steps below to set up and run the scripts.


```bash

## this is to download python on your system 
https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe

## paste on your browser to download git bash
https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe



## then click on your windows key and search for git bash then open it 
### 1. Clone the Repository
git clone https://github.com/Incrisz/geophysics-Spectral-analysis-program.git
cd geophysics-Spectral-analysis-program

## On Windows:
python -m venv myenv
source myenv/Scripts/activate

## 3. Install Dependencies
python -m pip install --upgrade pip
pip install numpy pandas matplotlib scipy openpyxl



## 4. Run Scripts
## To run any of the scripts, simply use the following command:


python <script_name>.py

## Example:
python guyok.py      # Run Guyok script
python kaltungo.py   # Run Kaltungo script
python dong.py      # Run Momgo script
python lau.py        # Run Lau script










## 2. Set Up a Virtual Environment
## On Linux/macOS:
# apt install python3.12-venv
git clone https://github.com/Incrisz/geophysics-Spectral-analysis-program.git
cd geophysics-Spectral-analysis-program
python3 -m venv myenv
source myenv/bin/activate

## 3. Install Dependencies
pip install numpy pandas matplotlib scipy openpyxl 




## This is for the web
## On Linux/macOS:
git clone https://github.com/Incrisz/geophysics-Spectral-analysis-program.git
cd geophysics-Spectral-analysis-program
apt install python3.12-venv
python3 -m venv myenv
source myenv/bin/activate

## 3. Install Dependencies
pip install numpy pandas matplotlib scipy openpyxl streamlit

## run it 
streamlit run web.py
