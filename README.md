# Code Complexity Analyzer

This project provides a simple command line tool for analyzing Python source files.
It computes cyclomatic complexity and nesting depth for each function, detects
similar functions, and generates an HTML report.

## Usage

```
python3 -m codecomplexity.cli path/to/file.py -o report.html
```

Open the generated `report.html` in your browser to view the results.

