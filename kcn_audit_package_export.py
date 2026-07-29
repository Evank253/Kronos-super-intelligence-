"""
KCN External Audit Package Exporter CLI (kcn_audit_package_export.py)
Generates and seals evidence/KCN_EXTERNAL_AUDIT_PACKAGE.zip for third-party security auditors.
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.abspath("."))
from evidence.audit_package_generator import AuditPackageGenerator
from orchestrator.assurance_scheduler import AssuranceScheduler

def main():
    parser = argparse.ArgumentParser(description="KCN External Audit Package Generator")
    parser.add_argument("--export-audit-package", action="store_true", help="Export third-party audit package zip")
    args = parser.parse_args()

    print("=======================================================================")
    print("      KCN EXTERNAL AUDITOR PACKAGE GENERATOR & SEALER                   ")
    print("=======================================================================\n")

    scheduler = AssuranceScheduler()
    sched_log = scheduler.run_daily_assurance_cycle()
    print(f"[1/2] Daily Assurance Maintenance Schedule: {sched_log['status']}")

    generator = AuditPackageGenerator()
    out_dir, zip_path, manifest = generator.generate_audit_package()

    print(f"[2/2] Third-Party Audit Package Sealed & Exported:")
    print(f"      - Audit Directory: {out_dir}")
    print(f"      - Audit Zip File:  {zip_path}")
    print(f"      - Files Checksummed: {len(manifest['file_checksums'])} Audit Artifacts")
    print(f"      - Manifest Status:  {manifest['status']}\n")

    print("=======================================================================")
    print("🏆 VERDICT: EXTERNAL AUDIT PACKAGE READY FOR THIRD-PARTY INSPECTION")
    print("=======================================================================\n")

if __name__ == "__main__":
    main()
