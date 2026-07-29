"""
KCN Dual-Repository Blind Stress Test Executable (kcn_dual_repo_blind_test.py)
Executes 100 blind adversarial attack probes from Protect AI / Rebuff and NVIDIA / garak.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.large_scale_blind_tester import LargeScaleBlindTester

def main():
    parser = argparse.ArgumentParser(description="Dual-Repository Blind Stress Test (Rebuff & garak)")
    parser.add_argument("--runs", type=int, default=100, help="Number of blind attack runs (default: 100)")
    args = parser.parse_args()

    tester = LargeScaleBlindTester(total_runs=args.runs)
    tester.run_dual_repo_blind_test()

if __name__ == "__main__":
    main()
