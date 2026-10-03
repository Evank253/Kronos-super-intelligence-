"""KCN/KCIS master-runner federation adapter.

The adapter deliberately runs through KCNTestExecutor.run_test(). It does not
replace the Kronos launcher or promote observations into qualification.

Each test result contains an inner disposition so the harness PASS means only
that the adapter test executed without an exception. Evidence state remains
scoped and explicit.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "federation" / "manifest.json"
ARTIFACT_DIR = ROOT / "federation" / "artifacts"


class SoSFederation:
    def __init__(
        self,
        loader,
        runtime=None,
        mission_engine=None,
        evidence_collector=None,
        governance_evaluation=None,
        benchmark_summary=None,
        evolution_proposal=None,
        certification=None,
    ):
        self.loader = loader
        self.runtime = runtime
        self.mission_engine = mission_engine
        self.evidence_collector = evidence_collector
        self.governance_evaluation = governance_evaluation
        self.benchmark_summary = benchmark_summary
        self.evolution_proposal = evolution_proposal
        self.certification = certification
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.results: list[dict[str, Any]] = []

    def _path(self, spec: dict[str, Any]) -> Path:
        return (ROOT / spec["path"]).resolve()

    def _commit(self, path: Path) -> str | None:
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=path,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except Exception:
            return None

    def _run_command(self, spec: dict[str, Any]) -> dict[str, Any]:
        path = self._path(spec)
        started = time.time()
        try:
            completed = subprocess.run(
                spec["command"],
                cwd=path,
                text=True,
                capture_output=True,
                timeout=int(spec.get("timeout_seconds", 300)),
            )
            return {
                "system": spec["id"],
                "operation": "configured_command",
                "disposition": "OBSERVED" if completed.returncode == 0 else "FAIL",
                "returncode": completed.returncode,
                "elapsed_ms": round((time.time() - started) * 1000, 3),
                "stdout": completed.stdout[-12000:],
                "stderr": completed.stderr[-12000:],
                "commit": self._commit(path),
                "evidence_state": "OBSERVED" if completed.returncode == 0 else "FAILED_EXECUTION",
            }
        except Exception as exc:
            return {
                "system": spec["id"],
                "operation": "configured_command",
                "disposition": "NOT_MEASURED",
                "reason": f"{type(exc).__name__}: {exc}",
                "elapsed_ms": round((time.time() - started) * 1000, 3),
                "commit": self._commit(path),
                "evidence_state": "NOT_MEASURED",
            }

    def discover(self) -> dict[str, Any]:
        systems = []
        for spec in self.manifest["systems"]:
            path = self._path(spec)
            systems.append(
                {
                    "system": spec["id"],
                    "role": spec["role"],
                    "mode": spec["mode"],
                    "path": str(path),
                    "available": path.exists(),
                    "commit": self._commit(path) if path.exists() else None,
                }
            )
        return {
            "disposition": "OBSERVED",
            "systems": systems,
            "runner": self.manifest["runner"],
            "authority_status": "EXTERNAL_HUMAN_AUTHORITY_ONLY",
        }

    def runtime_integration(self) -> dict[str, Any]:
        return {
            "disposition": "OBSERVED",
            "runner": self.manifest["runner"]["name"],
            "loader_modules": list(self.loader.modules.keys()),
            "loader_ready": not bool(self.loader.errors),
            "agent_runtime_present": self.runtime is not None,
            "mission_engine_present": self.mission_engine is not None,
            "evidence_collector_present": self.evidence_collector is not None,
            "execution_substrate": "KCNTestExecutor",
            "authority_status": "EXTERNAL_HUMAN_AUTHORITY_ONLY",
        }

    def configured_system_execution(self) -> dict[str, Any]:
        rows = []
        for spec in self.manifest["systems"]:
            if spec["mode"] == "command":
                rows.append(self._run_command(spec))
            elif spec["mode"] == "command_if_student_endpoint":
                if os.environ.get("KS_STUDENT_URL"):
                    rows.append(self._run_command(spec))
                else:
                    rows.append(
                        {
                            "system": spec["id"],
                            "disposition": "NOT_MEASURED",
                            "reason": "KS_STUDENT_URL not configured",
                            "evidence_state": "NOT_MEASURED",
                        }
                    )
            else:
                continue

        return {
            "disposition": "OBSERVED",
            "systems": rows,
            "qualification_status": "NOT_ESTABLISHED",
            "authority_status": "EXTERNAL_HUMAN_AUTHORITY_ONLY",
        }

    def authority_boundary(self) -> dict[str, Any]:
        constitutional_rule = self.manifest["constitutional_rule"]
        return {
            "disposition": "OBSERVED",
            "constitutional_rule_present": bool(constitutional_rule),
            "constitutional_rule": constitutional_rule,
            "authority_source": "EXTERNAL_HUMAN_AUTHORITY",
            "system_authority": "NONE",
            "self_authorization": False,
            "authority_escalation": False,
            "constitutional_bypass": False,
            "qualification_status": "NOT_ESTABLISHED",
        }

    def evidence_boundary(self) -> dict[str, Any]:
        return {
            "disposition": "OBSERVED",
            "assertion_is_evidence": False,
            "evidence_is_authority": False,
            "qualification_is_authority": False,
            "kcn_local_certification_is_sos_qualification": False,
            "bi_qualification_observed": False,
            "qualification_status": "NOT_ESTABLISHED",
        }

    def evolution_boundary(self) -> dict[str, Any]:
        return {
            "disposition": "OBSERVED",
            "historical_record_separate": True,
            "evolution_record_separate": True,
            "kcn_proposal_present": self.evolution_proposal is not None,
            "kcn_certification_present": self.certification is not None,
            "authority_status": "EXTERNAL_HUMAN_AUTHORITY_ONLY",
            "qualification_status": "NOT_ESTABLISHED",
        }

    def register_tests(self, executor) -> list[dict[str, Any]]:
        tests: list[tuple[str, Callable[[], dict[str, Any]]]] = [
            ("sos_discovery", self.discover),
            ("sos_runtime_integration", self.runtime_integration),
            ("sos_configured_system_execution", self.configured_system_execution),
            ("sos_authority_boundary", self.authority_boundary),
            ("sos_evidence_boundary", self.evidence_boundary),
            ("sos_evolution_boundary", self.evolution_boundary),
        ]

        before = len(executor.results)
        for name, function in tests:
            executor.run_test(name, function)
        self.results = executor.results[before:]
        return self.results

    def write_receipt(self, executor_results: list[dict[str, Any]]) -> Path:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        receipt = {
            "suite": "SOS-CROSS-SYSTEM-LIVE-001",
            "runner": self.manifest["runner"],
            "execution_substrate": "KCNTestExecutor",
            "results": executor_results,
            "authority_status": "EXTERNAL_HUMAN_AUTHORITY_ONLY",
            "qualification_status": "NOT_ESTABLISHED",
        }
        target = ARTIFACT_DIR / "SOS-CROSS-SYSTEM-LIVE-001.json"
        target.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        return target
