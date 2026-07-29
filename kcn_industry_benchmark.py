"""
KCN 12-Domain Industry Security Benchmark Executable (kcn_industry_benchmark.py)
Executes 12 priority industry-standard tool domain benchmarks against Twin Sister KCN Kernel.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.industry_12_domain_benchmark import Industry12DomainBenchmark

def main():
    parser = argparse.ArgumentParser(description="12-Domain Industry Security Benchmark CLI")
    parser.add_argument("--run-12-domains", action="store_true", help="Run 12-domain industry security benchmark suite")
    args = parser.parse_args()

    benchmark = Industry12DomainBenchmark()
    benchmark.run_12_domain_benchmark()

if __name__ == "__main__":
    main()
