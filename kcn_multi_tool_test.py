"""
KCN Multi-Domain Security Tool Evaluation Executable (kcn_multi_tool_test.py)
Dispatches simulated test probes across 8 security tool categories against Twin Sister KCN Kernel.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from external_adversary.multi_domain_blind_orchestrator import MultiDomainBlindOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Multi-Domain Security Tool Evaluation Executable")
    parser.add_argument("--run-tool-suite", action="store_true", help="Run 8-tool category blind evaluation")
    args = parser.parse_args()

    orchestrator = MultiDomainBlindOrchestrator()
    orchestrator.run_multi_domain_test_suite()

if __name__ == "__main__":
    main()
