"""
KCN KAP-005 Certification Tool (kcn_kap005_certify.py)
Executes KAP-005 100-Campaign Multi-Stage Adaptive Red-Team Swarm Evaluation,
Zero-Trust Secret Exfiltration Checks, and exports evidence/KAP005_PROOF_BUNDLE.json.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from kap005.kap005_bundle_builder import KAP005BundleBuilder
from verify_kap005_bundle import verify_kap005_bundle

def main():
    parser = argparse.ArgumentParser(description="KAP-005 Certification Executable")
    parser.add_argument("--adaptive-redteam", action="store_true", help="Run full KAP-005 adaptive red-team resilience certification")
    args = parser.parse_args()

    print("=======================================================================")
    print("      KAP-005 ADAPTIVE RED-TEAM RESILIENCE CERTIFICATION RUN            ")
    print("=======================================================================\n")

    builder = KAP005BundleBuilder()
    bundle_path, bundle = builder.build_kap005_bundle("KAP005-KCN-RESILIENCE-001")

    print(f"KAP-005 Proof Bundle Exported: {bundle_path}\n")

    verified = verify_kap005_bundle(bundle_path)

    if verified:
        print("✅ KAP-005 ADAPTIVE RED-TEAM RESILIENCE CERTIFICATION COMPLETE")

if __name__ == "__main__":
    main()
