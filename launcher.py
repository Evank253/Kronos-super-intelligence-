"""
KCN / KCIS Runtime Harness Master Launcher
Executes system discovery, component loading, capability benchmarks, agent runtime execution,
task graph missions, controlled self-improvement evolution, kernel scoring, and certification artifacts.
"""

import sys
import os
import json
from datetime import datetime, timezone

from runner.system_loader import KCNSystemLoader
from runner.test_executor import KCNTestExecutor
from adapters.mission_adapter import MissionAdapter
from adapters.agent_adapter import AgentAdapter
from reports.generator import ReportGenerator

from missions.engine import MissionEngine
from missions.mission_runner import MissionRunner
from missions.evidence_collector import EvidenceCollector
from missions.mission_validator import MissionValidator
from missions.task_graph import TaskGraph

from governance.approval_gate import ApprovalGate
from governance.approval_controller import ApprovalController

from learning.feedback_engine import FeedbackEngine
from learning.feedback_engine import FeedbackEngine as LearningFeedbackEngine
from learning.regression_tracker import RegressionTracker
from learning.learning_loop import LearningLoop

from scoring.kernel_score_engine import KernelScoreEngine
from scoring.certification import CertificationEngine

from discovery.module_scanner import ModuleScanner
from discovery.dependency_checker import DependencyChecker
from discovery.architecture_mapper import ArchitectureMapper
from reports.certification_report import CertificationReportGenerator
from reports.html_report import HTMLReportGenerator

from benchmarks.benchmark_engine import BenchmarkEngine
from evolution.improvement_engine import ImprovementEngine
from evolution.optimizer import EvolutionOptimizer
from evolution.proposal_manager import ProposalManager
from evolution.promotion_gate import PromotionGate

from agents.agent_runtime import AgentRuntime
from agents.agent_registry import AgentRegistry
from agents.agent_executor import AgentExecutor
from agents.kronos_agent import KronosAgent
from agents.astraea_agent import AstraeaAgent
from agents.hermes_agent import HermesAgent
from agents.prometheus_agent import PrometheusAgent
from dashboard.dashboard_data import DashboardData
from federation.sos_federation import SoSFederation

def main():
    print("=" * 70)
    print("     KCN / KCIS MASTER RUNTIME HARNESS & VALIDATION PIPELINE")
    print("=" * 70)

    # 1. Architecture Discovery
    print("\n[1/8] Discovering System Architecture & Environment...")
    scanner = ModuleScanner(".")
    scan_results = scanner.scan()
    print(f"   - Python Modules Found: {scan_results['modules_found']}")
    print(f"   - Agent Definitions: {scan_results['agents_found']}")
    print(f"   - API Endpoints: {scan_results['apis_found']}")

    dep_checker = DependencyChecker()
    dep_res = dep_checker.check()
    print(f"   - Environment Status: {dep_res['status']} ({dep_res['installed_count']} packages verified)")

    # 2. Component Loading
    print("\n[2/8] Loading KCN Core Modules...")
    loader = KCNSystemLoader()
    loader.load_kcn_core()
    health = loader.health_report()
    print(f"   - Loaded Core Modules: {', '.join(health['loaded_modules'])}")
    print(f"   - Core System Ready: {health['system_ready']}")

    # 3. Agent Runtime Initialization & Execution
    print("\n[3/8] Initializing Agent Runtime & Executable Agents...")
    runtime = AgentRuntime()
    runtime.register("Kronos", KronosAgent())
    runtime.register("Astraea", AstraeaAgent())
    runtime.register("Hermes", HermesAgent())
    runtime.register("Prometheus", PrometheusAgent())

    executor_log = AgentExecutor(runtime)
    agent_adapter = AgentAdapter(runtime)

    for agent_name in ["Kronos", "Astraea", "Hermes", "Prometheus"]:
        insp = agent_adapter.inspect_agent(agent_name)
        log_res = executor_log.execute_and_log(f"INIT-{agent_name}", agent_name, f"System readiness check for {agent_name}")
        print(f"   - Agent {agent_name:<11}: Registered={insp['registered']}, Executable={insp['execution']}")

    # 4. Capability Benchmark Engine
    print("\n[4/8] Executing Capability Benchmark Engine...")
    bm_engine = BenchmarkEngine()
    bm_summary = bm_engine.run_all("reports/KCN_CAPABILITY_SCORE.json", "evidence/benchmark_results.json")
    print(f"   - Memory Benchmark   : {bm_summary['memory']['score'] * 100:.0f}%")
    print(f"   - Agent Benchmark    : {bm_summary['agents']['score'] * 100:.0f}%")
    print(f"   - Security Benchmark : {bm_summary['security']['score'] * 100:.0f}%")
    print(f"   - Learning Benchmark : {bm_summary['learning']['score'] * 100:.0f}%")
    print(f"   - Governance Benchmark: {bm_summary['governance']['score'] * 100:.0f}%")

    # 5. Task Graph Mission Loop
    print("\n[5/8] Executing Task Graph Mission Loop...")
    engine_inst = MissionEngine(agent_runtime=runtime)
    m_runner = MissionRunner(engine_inst)
    mission = m_runner.create_mission("KCN Harness Full Validation", "Kronos")

    gate = ApprovalGate()
    gov_eval = gate.evaluate("deploy")
    print(f"   - Governance Gate Check ('deploy'): {gov_eval['state']}")

    executed_mission = m_runner.execute(mission)
    collector = EvidenceCollector()
    evidence = collector.collect(executed_mission)

    validator = MissionValidator()
    val_result = validator.validate(evidence)
    print(f"   - Mission Validation Score: {val_result['score'] * 100:.1f}%")

    # 6. Controlled Evolution & Improvement Loop
    print("\n[6/8] Running Controlled Self-Improvement Evolution Loop...")
    imp_engine = ImprovementEngine()
    imp_analysis = imp_engine.analyze(bm_summary)
    print(f"   - Weakest Capability Identified: {imp_analysis['target'].upper()} ({imp_analysis['current_score']*100:.0f}%)")

    optimizer = EvolutionOptimizer()
    opt_goal = optimizer.optimize(imp_analysis)

    proposal_mgr = ProposalManager()
    proposal = proposal_mgr.create(imp_analysis)
    print(f"   - Proposal Created: {proposal['proposal_id']} -> {proposal['status']}")

    prom_gate = PromotionGate()
    prom_eval = prom_gate.evaluate(proposal['status'])
    print(f"   - Promotion Gate Evaluation: {prom_eval['promotion']} ({prom_eval['state']})")

    # 7. Kernel Scoring & Certification
    print("\n[7/8] Evaluating KCN Kernel Readiness Rating...")
    subsystem_metrics = {
        "memory": bm_summary["memory"]["score"],
        "agents": bm_summary["agents"]["score"],
        "security": bm_summary["security"]["score"],
        "learning": bm_summary["learning"]["score"],
        "governance": bm_summary["governance"]["score"]
    }

    score_engine = KernelScoreEngine()
    calculated_score = score_engine.calculate(subsystem_metrics)

    cert_engine = CertificationEngine()
    certification = cert_engine.evaluate(calculated_score["overall_score"])

    print("   -------------------------------------------------------")
    print(f"   KCN KERNEL OVERALL READINESS SCORE: {calculated_score['overall_score']}%")
    print(f"   CERTIFICATION STATUS:              {certification['certification']}")
    print("   -------------------------------------------------------")
    for k, v in calculated_score["breakdown"].items():
        print(f"     * {k.capitalize():<12}: {v}")

    # 8. Report & Artifact Generation
    print("\n[8/8] Generating Certification Artifacts & Refreshing Command Center...")
    test_executor = KCNTestExecutor(loader)
    core_tests = test_executor.run_core_tests()

    # The existing KCNTestExecutor remains the sole benchmark execution
    # substrate. The SoS federation is registered as additional tests rather
    # than introducing a second runner.
    federation = SoSFederation(
        loader=loader,
        runtime=runtime,
        mission_engine=engine_inst,
        evidence_collector=collector,
        governance_evaluation=gov_eval,
        benchmark_summary=bm_summary,
        evolution_proposal=proposal,
        certification=certification,
    )
    sos_tests = federation.register_tests(test_executor)
    all_tests = core_tests + sos_tests
    federation_receipt = federation.write_receipt(sos_tests)
    print(f"   - SoS Federation Tests Executed: {len(sos_tests)}")
    print(f"   - SoS Receipt: {federation_receipt}")

    report_gen = ReportGenerator()
    report_gen.generate(loader, all_tests, "reports/KCN_SYSTEM_STATUS.json")

    cert_gen = CertificationReportGenerator()
    cert_gen.generate(calculated_score["breakdown"], certification, "reports/KCN_CERTIFICATION_REPORT.json")

    html_gen = HTMLReportGenerator()
    html_gen.generate({
        "timestamp": str(datetime.now(timezone.utc)),
        "certification": certification["certification"],
        "overall_score": calculated_score["overall_score"],
        "breakdown": calculated_score["breakdown"]
    }, "reports/kcn_validation_summary.html")

    db_data = DashboardData()
    data_summary = db_data.get_status()

    print("\n" + "=" * 70)
    print("✅ KCN VALIDATION, CERTIFICATION & EVOLUTION CYCLE COMPLETE")
    print("Artifacts generated & synced:")
    print(" - reports/KCN_SYSTEM_STATUS.json")
    print(" - reports/KCN_CERTIFICATION_REPORT.json")
    print(" - reports/KCN_CAPABILITY_SCORE.json")
    print(" - evidence/benchmark_results.json")
    print(" - evidence/improvement_history.json")
    print(" - evidence/agent_execution_log.json")
    print(" - dashboard/templates/index.html")
    print(" - dashboard/app.py (FastAPI Command Center)")
    print("=" * 70)

if __name__ == "__main__":
    main()
