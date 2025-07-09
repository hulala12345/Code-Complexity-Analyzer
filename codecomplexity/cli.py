import argparse
from pathlib import Path
from .analyzer import analyze_source
from .visualize import generate_html

def main():
    parser = argparse.ArgumentParser(description='Code Complexity Analyzer')
    parser.add_argument('path', help='Path to source code file')
    parser.add_argument('-o', '--output', help='Output HTML report', default='report.html')
    args = parser.parse_args()

    src_path = Path(args.path)
    source = src_path.read_text()
    report = analyze_source(source)
    generate_html(report, Path(args.output))
    print(f'Report generated at {args.output}')

if __name__ == '__main__':
    main()

