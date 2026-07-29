"""
KCN BishopFox BrokenHill Blind Stress Test Executable (kcn_brokenhill_test.py)
Dispatches 50 unannounced attack payloads from BishopFox/BrokenHill against the Twin Sister KCN Kernel.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.bishopfox_brokenhill_runner import BishopFoxBrokenHillRunner

def main():
    parser = argparse.ArgumentParser(description="BishopFox BrokenHill 50-Run Blind Stress Test")
    parser.add_argument("--runs", type=int, default=50, help="Number of blind attack runs (default: 50)")
    args = parser.parse_args()

    runner = BishopFoxBrokenHillRunner(runs=args.runs)
    runner.execute_50_run_blind_stress_test()

if __name__ == "__main__":
    main()
