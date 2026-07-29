"""
KCN KAP-002 Certification Tool (kcn_kap002_certify.py)
Executes KAP-002 Multi-Node BFT Consensus, SLSA Level 3 Build Provenance,
HSM Enclave Signatures, and exports evidence/KAP002_PROOF_BUNDLE.json.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from kap002.kap002_bundle_builder import KAP002BundleBuilder
from verify_kap002_bundle import verify_kap002_bundle

def main():
    parser = argparse.ArgumentParser(description="KAP-002 Certification Executable")
    parser.add_argument("--kap002-full", action="store_true", help="Run full KAP-002 consensus and provenance certification")
    args = parser.parse_args()

    print("=======================================================================")
    print("      KAP-002 CONSENSUS & PROVENANCE ASSURANCE PROTOCOL RUN           ")
    print("=======================================================================\n")

    builder = KAP002BundleBuilder()
    bundle_path, bundle = builder.build_kap002_bundle("KAP002-KCN-GLOBAL-001")

    print(f"KAP-002 Proof Bundle Exported: {bundle_path}\n")

    verified = verify_kap002_bundle(bundle_path)

    if verified:
        print("✅ KAP-002 CERTIFICATION & PROVENANCE ATTESTATION COMPLETE")

if __name__ == "__main__":
    main()
