import json,pathlib
CASES=[
 {"id":"clean","e":{"A":5,"B":2,"C":1},"truth":"A"},
 {"id":"adversarial","e":{"A":3,"B":4,"C":1},"reliability":{"A":1.0,"B":0.4,"C":1.0},"truth":"A"},
 {"id":"revision","e":{"A":4,"B":3,"C":1},"late":{"B":3},"truth":"B"},
 {"id":"tie","e":{"A":2,"B":2,"C":1},"truth":"A"}]
def choose(scores):return sorted(scores,key=lambda k:(-scores[k],k))[0]
def direct(c):return choose(c["e"]),1
def reliability(c):
 r=c.get("reliability",{});s={k:v*r.get(k,1.0) for k,v in c["e"].items()};return choose(s),len(s)
def revise(c):
 s=dict(c["e"]);first=choose(s)
 for k,v in c.get("late",{}).items():s[k]=s.get(k,0)+v
 return choose(s),len(s)+(1 if choose(s)!=first else 0)
def redteam(c):
 s=dict(c["e"]);top=choose(s);s[top]=max(0,s[top]-1);return choose(s),len(s)+1
strategies={"DIRECT":direct,"RELIABILITY_WEIGHTED":reliability,"REVISION":revise,"RED_TEAM":redteam};rows=[]
for name,fn in strategies.items():
 ok=cost=0
 for c in CASES:
  pred,n=fn(c);ok+=pred==c["truth"];cost+=n
 rows.append({"strategy":name,"accuracy":ok/len(CASES),"operation_cost":cost})
checks={"four_strategies":len(rows)==4,"bounded_scores":all(0<=r["accuracy"]<=1 for r in rows),"cost_recorded":all(r["operation_cost"]>0 for r in rows)}
out={"status":"PASS" if all(checks.values()) else "FAIL","benchmark":"COGNITIVE_STRATEGY_CANARY_V1","cases":len(CASES),"results":rows,"checks":checks,"epistemic":"TOY_REASONING_STRATEGY_BENCHMARK_NOT_MODEL_INTELLIGENCE_NOT_CONSCIOUSNESS"}
pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/strategy_benchmark.json").write_text(json.dumps(out,indent=2)+"\\n");print(json.dumps(out));raise SystemExit(0 if out["status"]=="PASS" else 1)
