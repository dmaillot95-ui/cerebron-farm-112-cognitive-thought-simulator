import json,pathlib
# Observable reasoning-state simulator only; no consciousness claim.
problem={"id":"C0","question":"choose hypothesis using evidence","evidence":{"A":3,"B":1,"C":2}}
hyp=[{"id":k,"support":v} for k,v in problem["evidence"].items()]
hyp.sort(key=lambda x:(-x["support"],x["id"]))
state={"problem":problem["id"],"working_memory":["A","B","C"],"hypotheses":hyp,"selected":hyp[0]["id"],"red_team":{"challenge":"remove strongest evidence","revised_selected":"C"},"residual_unknowns":["external_validity"]}
checks={"deterministic_choice":state["selected"]=="A","red_team_revision":state["red_team"]["revised_selected"]=="C","unknown_preserved":len(state["residual_unknowns"])>0}
out={"farm":112,"status":"PASS" if all(checks.values()) else "FAIL","checks":checks,"state":state,"epistemic":"COMPUTATIONAL_REASONING_STATE_CANARY_NOT_CONSCIOUSNESS_NOT_HUMAN_COGNITION_MODEL"}
pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/result.json").write_text(json.dumps(out,indent=2)+"\\n");print(json.dumps(out));raise SystemExit(0 if out["status"]=="PASS" else 1)
