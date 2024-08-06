#!/bin/bash

# Simple script to create a virtual environment and
# install the required packages

mkdir tracks
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Virtual environment created and packages installed"
