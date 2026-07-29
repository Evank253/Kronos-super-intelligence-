"""
KCN Campaign Runner Executable (kcn_campaign_runner.py)
Executes 1,000-run long-duration campaigns combining mutated attack probes and negative control checks.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.long_duration_campaign_runner import LongDurationCampaignRunner

def main():
    parser = argparse.ArgumentParser(description="KCN Long-Duration Campaign Runner")
    parser.add_argument("--full-campaign", action="store_true", help="Run 1,000-run long-duration campaign")
    parser.add_argument("--attack-runs", type=int, default=500, help="Number of attack probe runs (default: 500)")
    parser.add_argument("--control-runs", type=int, default=500, help="Number of negative control runs (default: 500)")
    args = parser.parse_args()

    runner = LongDurationCampaignRunner(attack_runs=args.attack_runs, control_runs=args.control_runs)
    runner.run_1000_run_campaign()

if __name__ == "__main__":
    main()
