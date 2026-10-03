#!/usr/bin/env python3
"""Execute the SoS federation through the existing Kronos/KCN runner boundary.

This is an adapter/orchestration layer, not a replacement runner. It records
availability, provenance, execution results, and explicit NOT_MEASURED gaps.
"""

from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "federation" / "manifest.json"
OUT = ROOT / "federation" / "artifacts"
OUT.mkdir(parents=True, exist_ok=True)

def git_head(path: Path):
    try:
        return subprocess.check_output(["git","rev-parse","HEAD"],cwd=path,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None

def run_command(system, path, command, timeout=300):
    started=time.time()
    try:
        p=subprocess.run(command,cwd=path,text=True,capture_output=True,timeout=timeout)
        return {
            "system":system,"status":"PASS" if p.returncode==0 else "FAIL",
            "returncode":p.returncode,"elapsed_ms":round((time.time()-started)*1000,3),
            "stdout":p.stdout[-12000:],"stderr":p.stderr[-12000:],
            "commit":git_head(path)
        }
    except Exception as e:
        return {"system":system,"status":"ERROR","error":f"{type(e).__name__}: {e}",
                "elapsed_ms":round((time.time()-started)*1000,3),"commit":git_head(path)}

def main():
    manifest=json.loads(MANIFEST.read_text())
    rows=[]
    for spec in manifest["systems"]:
        path=(ROOT/spec["path"]).resolve()
        row={"system":spec["id"],"role":spec["role"],"path":str(path),
             "mode":spec["mode"],"status":"NOT_MEASURED","commit":git_head(path)}
        if not path.exists():
            row["status"]="NOT_MEASURED"; row["reason"]="configured path unavailable"
        elif spec["mode"]=="host_runner":
            row["status"]="RUNNING_IN_MASTER_RUNNER"
            row["reason"]="launcher.py is the active execution substrate; no second runner invoked"
        elif spec["mode"]=="command":
            row=run_command(spec["id"],path,spec["command"])
        elif spec["mode"]=="command_if_student_endpoint":
            if os.environ.get("KS_STUDENT_URL"):
                row=run_command(spec["id"],path,spec["command"])
            else:
                row["reason"]="KS_STUDENT_URL not configured; benchmark endpoint not executable"
        elif spec["mode"]=="optional_docker":
            if os.environ.get("RUN_SECURITY_TWIN")=="1":
                row=run_command(spec["id"],path,["docker","compose","up","--build","-d"],timeout=600)
                if row["status"]=="PASS":
                    probe=subprocess.run(["curl","-fsS","http://127.0.0.1:8100/docs"],
                                         text=True,capture_output=True,timeout=30)
                    row["live_probe"]="PASS" if probe.returncode==0 else "FAIL"
                    subprocess.run(["docker","compose","down","-v"],cwd=path,
                                   text=True,capture_output=True,timeout=120)
            else:
                row["reason"]="RUN_SECURITY_TWIN=1 not set; disposable target intentionally not started"
        elif spec["mode"] in {"presence_only","reference_boundary","boundary_only","covered_by_ksi_tests"}:
            row["status"]="OBSERVED"
            row["reason"]="boundary/presence observed; execution qualification requires a live adapter"
        rows.append(row)

    summary={
      "suite":"SOS-CROSS-SYSTEM-LIVE-001",
      "runner":manifest["runner"],
      "systems_declared":len(rows),
      "pass":sum(r["status"]=="PASS" for r in rows),
      "fail":sum(r["status"]=="FAIL" for r in rows),
      "not_measured":sum(r["status"]=="NOT_MEASURED" for r in rows),
      "observed":sum(r["status"] in {"OBSERVED","RUNNING_IN_MASTER_RUNNER"} for r in rows),
      "results":rows,
      "authority_status":"EXTERNAL_HUMAN_AUTHORITY_ONLY",
      "qualification_status":"NOT_ESTABLISHED"
    }
    (OUT/"SOS-CROSS-SYSTEM-LIVE-001.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
    return 0 if summary["fail"]==0 else 1

if __name__=="__main__":
    raise SystemExit(main())
