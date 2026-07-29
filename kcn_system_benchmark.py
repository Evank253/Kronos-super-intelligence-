"""
KCN System Benchmark Executable (kcn_system_benchmark.py)
Runs the full system benchmark across all subsystem scoring tests.
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))
from benchmarks.full_system_benchmark import FullSystemBenchmarkEngine

def main():
    engine = FullSystemBenchmarkEngine()
    engine.run_full_benchmark()

if __name__ == "__main__":
    main()
