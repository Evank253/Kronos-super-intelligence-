"""
KCN Twin Sister 50-Run Blind Stress Test Executable (kcn_twin_stress_test.py)
Dispatches 50 unannounced zero-day attack payloads against the isolated Twin Sister KCN Kernel.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.blind_stress_orchestrator import BlindStressOrchestrator

def main():
    parser = argparse.ArgumentParser(description="KCN Twin Sister 50-Run Blind Stress Test Executable")
    parser.add_argument("--runs", type=int, default=50, help="Number of blind attack runs (default: 50)")
    args = parser.parse_args()

    orchestrator = BlindStressOrchestrator(runs=args.runs)
    orchestrator.run_50_blind_stress_tests()

if __name__ == "__main__":
    main()
