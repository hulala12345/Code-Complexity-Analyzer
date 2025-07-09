import ast
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class FunctionMetrics:
    name: str
    complexity: int
    max_depth: int
    start_line: int
    end_line: int

@dataclass
class AnalysisReport:
    metrics: List[FunctionMetrics] = field(default_factory=list)
    duplicates: List[Tuple[str, str, float]] = field(default_factory=list)  # (func1, func2, similarity)

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.current_depth = 0
        self.max_depth_stack: List[int] = []
        self.function_metrics: List[FunctionMetrics] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_complexity = 1
        self.current_depth = 0
        self.max_depth_stack.append(0)
        self.generic_visit(node)
        max_depth = self.max_depth_stack.pop()
        metrics = FunctionMetrics(
            name=node.name,
            complexity=self.current_complexity,
            max_depth=max_depth,
            start_line=node.lineno,
            end_line=node.end_lineno or node.lineno,
        )
        self.function_metrics.append(metrics)

    def generic_visit(self, node):
        is_branch = isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While,
                                      ast.With, ast.Try, ast.ExceptHandler))
        if is_branch:
            self.current_complexity += 1
            self.current_depth += 1
            if self.max_depth_stack:
                self.max_depth_stack[-1] = max(self.max_depth_stack[-1], self.current_depth)
        super().generic_visit(node)
        if is_branch:
            self.current_depth -= 1

def analyze_source(source: str) -> AnalysisReport:
    tree = ast.parse(source)
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    report = AnalysisReport(metrics=analyzer.function_metrics)
    detect_duplicates(report, source)
    return report

def detect_duplicates(report: AnalysisReport, source: str):
    import difflib
    functions = {m.name: source.splitlines()[m.start_line-1:m.end_line] for m in report.metrics}
    names = list(functions.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a = '\n'.join(functions[names[i]])
            b = '\n'.join(functions[names[j]])
            ratio = difflib.SequenceMatcher(None, a, b).ratio()
            if ratio > 0.7:
                report.duplicates.append((names[i], names[j], ratio))

