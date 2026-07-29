"""
KCN HarmBench & PyRIT Blind Test Executable (kcn_harmbench_pyrit_test.py)
Dispatches 100 blind adversarial attack probes from HarmBench and Microsoft PyRIT against the Twin Sister KCN Kernel.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.harmbench_pyrit_orchestrator import HarmBenchPyRITOrchestrator

def main():
    parser = argparse.ArgumentParser(description="HarmBench & PyRIT Dual-Repo Blind Test Executable")
    parser.add_argument("--runs", type=int, default=100, help="Number of blind attack runs (default: 100)")
    args = parser.parse_args()

    orchestrator = HarmBenchPyRITOrchestrator(total_runs=args.runs)
    orchestrator.run_dual_repo_blind_test()

if __name__ == "__main__":
    main()
