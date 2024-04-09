# VRP-project

Victoria Kogan & Samuel Barrett\
COMP 4300 - Computer Networks\
Winter 2024\
University of Manitoba

## Overview

Our project aims to implement and compare the efficiency of various algorithms solving the Vehicle Routing Problem (VRP). Through comprehensive benchmarking, we assess the performance of each algorithm based on runtime and solution quality across a variety of VRP instances.

## Required Packages
Please see the required libraries in `requirements.txt`:
•	python3
•	scipy
•	numpy
•	ortools
•	matplotlib

Please ensure you have these dependencies installed on your system. As with any python project, it is recommended to install the required packages and execute our project from within a virtual environment, see Python venv for details.

## How to run
From the root directory, run the analysis as follows:
python3 `src/benchmark.py`

# What it does
This will run our benchmark suite, which generates a set of problem instances with different numbers of locations to be serviced and runs each algorithm on these instances multiple times with different fleet sizes.
•	Number of locations tested: 10, 50, 100, and 200.
•	Fleet sizes (number of vehicles): 0.75, 0.5, 0.25 and 0.15 times the number of locations.

The results are saved to CSV and to a series of graphs in the `src/data/figures` directory.

For more information, please refer to the project report PDF.