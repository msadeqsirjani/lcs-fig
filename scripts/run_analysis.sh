#!/bin/bash

# Script to generate HTML reports from algorithm results
# Author: Created by AI Assistant

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

python3 ./src/generate_report.py --results-dir results/comparison_results --output report.html

deactivate