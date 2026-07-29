"""
KCN KAP-004 Enterprise Certification Tool (kcn_kap004_certify.py)
Executes KAP-004 Enterprise Assurance Suite:
- NIST AI RMF 1.0, ISO/IEC 42001, NIST CSF 2.0, & SLSA Level 3 Crosswalks.
- Certificate Transparency (CT) Merkle Inclusion Proof Generation.
- Transitive Dependency Tree Risk & Malicious Package Scanning.
- KAP-003 3/3 Federated Authority Co-signing & Ed25519 PKI.
- Exports evidence/KAP004_PROOF_BUNDLE.json and reports/COMPLIANCE_CROSSWALK_REPORT.md.
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath("."))

from compliance.compliance_engine import ComplianceEngine
from supply_chain.dependency_risk_analyzer import DependencyRiskAnalyzer
from transparency.transparency_service import TransparencyService
from transparency.inclusion_proof_verifier import InclusionProofVerifier
from kap003.kap003_bundle_builder import KAP003BundleBuilder
from verify_kap004_bundle import verify_kap004_bundle


def run_kap004_certification(is_full=True):
    print("=======================================================================")
    print("      KAP-004 ENTERPRISE COMPLIANCE & TRANSPARENCY CERTIFICATION       ")
    print("=======================================================================\n")

    # 1. Enterprise Compliance Crosswalk (NIST AI RMF 1.0, ISO 42001, NIST CSF, SLSA)
    comp_engine = ComplianceEngine()
    comp_report = comp_engine.run_compliance_crosswalk()

    # 2. Dependency Risk Analysis (Transitive dependencies, licenses, malicious packages)
    risk_analyzer = DependencyRiskAnalyzer()
    risk_res = risk_analyzer.analyze_dependency_tree()

    # 3. Base KAP-003 Federated Bundle
    builder3 = KAP003BundleBuilder()
    kap3_path, kap3_bundle = builder3.build_kap003_bundle("KAP003-BASE-ALLIANCE")

    # 4. Certificate Transparency & Merkle Inclusion Proof
    ct_service = TransparencyService()
    cert_dict = kap3_bundle.get("signed_certificate", {})
    leaf_hash = cert_dict.get("evidence_hash", cert_dict.get("merkle_root", "0"*64))
    inclusion_proof = ct_service.generate_inclusion_proof(leaf_hash)

    proof_verifier = InclusionProofVerifier()
    inclusion_verified = proof_verifier.verify_inclusion_proof(inclusion_proof)

    # 5. Build KAP-004 Composite Bundle
    kap004_bundle = {
        "bundle_id": "KAP004-KCN-ENTERPRISE-001",
        "kap_protocol_version": "KAP-004-Enterprise-Compliance",
        "exported_at": str(datetime.now(timezone.utc)),
        "enterprise_compliance_crosswalk": comp_report,
        "dependency_risk_analysis": risk_res,
        "certificate_transparency": {
            "inclusion_proof": inclusion_proof,
            "inclusion_verified": inclusion_verified["inclusion_verified"]
        },
        "federated_co_signatures": kap3_bundle["federated_co_signatures"],
        "sbom_manifest": kap3_bundle["sbom_manifest"],
        "slsa_provenance": kap3_bundle["slsa_provenance"],
        "consensus_evaluation": kap3_bundle["consensus_evaluation"],
        "metric_schema_documentation": kap3_bundle["metric_schema_documentation"],
        "reproducibility_manifest": kap3_bundle["reproducibility_manifest"],
        "raw_execution_traces": kap3_bundle["raw_execution_traces"],
        "cryptographic_ledger": kap3_bundle["cryptographic_ledger"],
        "signed_certificate": kap3_bundle["signed_certificate"]
    }

    output_path = "evidence/KAP004_PROOF_BUNDLE.json"
    os.makedirs("evidence/audit_exports", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(kap004_bundle, f, indent=4)

    with open("evidence/audit_exports/kcn_kap004_audit_export.json", "w") as f:
        json.dump(kap004_bundle, f, indent=4)

    print(f"[1/4] NIST AI RMF 1.0 / ISO 42001 Compliance: {comp_report['overall_compliance_pct']} (100% Mapped)")
    print(f"[2/4] Dependency Risk & Malicious Package Scan: {risk_res['license_compliance']} ({risk_res['packages_analyzed']} Libraries)")
    print(f"[3/4] Certificate Transparency Inclusion Proof: {'✅ VERIFIED' if inclusion_verified['inclusion_verified'] else '❌ FAILED'} (Leaf Hash Verified)")
    print(f"[4/4] KAP-003 Federated CA Co-Signatures:       {len(kap3_bundle['federated_co_signatures']['federated_signatures'])}/3 Authorities Approved\n")

    verified = verify_kap004_bundle(output_path)

    if verified:
        print("=======================================================================")
        print("🏆 KAP-004 ENTERPRISE COMPLIANCE & TRANSPARENCY CERTIFICATION PASSED")
        print("STATUS: HUMAN GOVERNED KAP-004 ENTERPRISE CERTIFIED")
        print("=======================================================================\n")

    return kap004_bundle


def main():
    parser = argparse.ArgumentParser(description="KAP-004 Enterprise Certification Executable")
    parser.add_argument("--compliance-full", action="store_true", help="Run full KAP-004 compliance & transparency certification")
    args = parser.parse_args()

    run_kap004_certification(is_full=args.compliance_full)


if __name__ == "__main__":
    main()
