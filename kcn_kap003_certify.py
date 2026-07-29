"""
KCN KAP-003 Federated Certification Tool (kcn_kap003_certify.py)
Executes KAP-003 3/3 Federated Authority Co-signing, CycloneDX/SPDX SBOM generation,
SLSA Level 3 Build Provenance, BFT Consensus, and exports evidence/KAP003_PROOF_BUNDLE.json.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from kap003.kap003_bundle_builder import KAP003BundleBuilder
from verify_kap003_bundle import verify_kap003_bundle

def main():
    parser = argparse.ArgumentParser(description="KAP-003 Federated Certification Executable")
    parser.add_argument("--federated-full", action="store_true", help="Run full KAP-003 federated alliance certification")
    args = parser.parse_args()

    print("=======================================================================")
    print("      KAP-003 OPEN ALLIANCE FEDERATED CERTIFICATION RUN                ")
    print("=======================================================================\n")

    builder = KAP003BundleBuilder()
    bundle_path, bundle = builder.build_kap003_bundle("KAP003-KCN-ALLIANCE-001")

    print(f"KAP-003 Proof Bundle Exported: {bundle_path}\n")

    verified = verify_kap003_bundle(bundle_path)

    if verified:
        print("✅ KAP-003 FEDERATED CERTIFICATION & MUTUAL TRUST ATTESTATION COMPLETE")

if __name__ == "__main__":
    main()
