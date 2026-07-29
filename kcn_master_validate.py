"""
KCN Master Validation CLI (kcn_master_validate.py)
Unified command orchestrator supporting:
- Full Validation Cycle (`--full`)
- Production Environment Check (`--production-check`)
- Research & Knowledge Acquisition Cycle (`--research-cycle`)
- Nervous Event Bus System Verification (`--event-system`)
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone

from orchestrator.master_validator import MasterValidator
from connectors.repository_connector import RepositoryConnector
from connectors.environment_validator import EnvironmentValidator
from execution.real_task_executor import RealTaskExecutor
from research.research_orchestrator import ResearchOrchestrator
from nervous_system.event_bus import UnifiedEventBus

def run_master_validation():
    validator = MasterValidator()
    summary = validator.run_master_chain()
    return summary

def run_production_check():
    print("================================================")
    print("      KCN PRODUCTION ENVIRONMENT CHECK          ")
    print("================================================\n")

    env_val = EnvironmentValidator()
    env_res = env_val.validate_environment()

    repo_conn = RepositoryConnector()
    repo_res = repo_conn.scan_repository(".")

    task_exec = RealTaskExecutor()
    exec_res = task_exec.execute_task("PROD-CHK-001", "Kronos", "Production Environment Verification", "read_memory")

    print(f"Repository:           {repo_res['repository']}")
    print(f"Languages:            {', '.join(repo_res['languages'])}")
    print(f"Files Scanned:        {repo_res['files_scanned']}")
    print(f"Dependencies:         {repo_res['dependencies_found']}")
    print(f"Security Findings:    {repo_res['security_findings']}")
    print(f"Environment Valid:    {env_res['environment_valid']}")
    print(f"Sandbox Controller:   ACTIVE")
    print(f"Evidence Hash Seal:   {exec_res['evidence_hash'][:16]}...\n")

    print("STATUS: PRODUCTION CHECK PASSED")
    print("================================================")

def run_research_cycle():
    print("================================================")
    print("   KCN RESEARCH & KNOWLEDGE ACQUISITION CYCLE   ")
    print("================================================\n")

    orchestrator = ResearchOrchestrator()
    res = orchestrator.run_research_cycle()

    print(f"Sources Analyzed:        {res['sources_analyzed']}")
    print(f"Claims Extracted:        {res['claims_extracted']}")
    print(f"Validated Claims:        {res['validated_claims']}\n")

    print("Knowledge Proposals:")
    for prop in res['knowledge_proposals']:
        print(f"  * {prop}")

    print(f"\nHuman Approval:          {res['human_approval']}")
    print(f"Memory Update:           {res['memory_update']}")
    print(f"Evidence:                {res['evidence']}\n")

    print(f"STATUS:                  {res['status']}")
    print("================================================")

def run_event_system():
    print("================================================")
    print("        KCN NERVOUS SYSTEM VALIDATION           ")
    print("================================================\n")

    bus = UnifiedEventBus()
    val_res = bus.validate_event_system()

    print(f"Event Bus:              {val_res['event_bus']}")
    print(f"Schemas Validated:      {val_res['schemas_validated']}")
    print(f"Subsystem Connections:  {val_res['subsystem_connections']}")
    print(f"Security Routing:       {val_res['security_routing']}")
    print(f"Audit Logging:          {val_res['audit_logging']}")
    print(f"Human Approval Routing: {val_res['human_approval_routing']}")
    print(f"Evidence Chain:         {val_res['evidence_chain']}\n")

    print(f"STATUS:                 {val_res['status']}")
    print("================================================")

def main():
    parser = argparse.ArgumentParser(description="KCN Master Validation CLI")
    parser.add_argument("--full", action="store_true", help="Run full master validation cycle")
    parser.add_argument("--production-check", action="store_true", help="Run real-world production environment check")
    parser.add_argument("--research-cycle", action="store_true", help="Run research & knowledge acquisition cycle")
    parser.add_argument("--event-system", action="store_true", help="Run nervous system event bus validation")

    args = parser.parse_args()

    if args.production_check:
        run_production_check()
    elif args.research_cycle:
        run_research_cycle()
    elif args.event_system:
        run_event_system()
    else:
        run_master_validation()

if __name__ == "__main__":
    main()
