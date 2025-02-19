import sys
import os
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

try:
    import pandas as pd
    print("Successfully imported pandas")
except ImportError as e:
    print(f"Failed to import pandas: {e}")

try:
    import pydantic
    print("Successfully imported pydantic")
except ImportError as e:
    print(f"Failed to import pydantic: {e}")

# Try to read a file
try:
    with open("data/input/drugs.csv", "r") as f:
        print("First line of drugs.csv:", f.readline().strip())
except Exception as e:
    print(f"Error reading drugs.csv: {e}")