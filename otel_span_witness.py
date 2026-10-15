"""Offline, bounded captured-input analysis. Original implementation, MIT."""
import argparse
import json
import re
import sys
from pathlib import Path

class InputError(ValueError):
    pass

def obj(x,required,optional=()):
    if not isinstance(x,dict) or set(x)-set(required)-set(optional) or set(required)-set(x):
        raise InputError("object keys do not match the documented contract")
    return x

def arr(x,limit=512):
    if not isinstance(x,list) or len(x)>limit:raise InputError("expected a bounded array")
    return x

def text(x):
    if not isinstance(x,str) or not 1<=len(x)<=256:raise InputError("expected a nonempty string <=256 characters")
    return x

def integer(x,maximum=9223372036854775807):
    if type(x) is not int or not 0<=x<=maximum:raise InputError("expected bounded nonnegative integer")
    return x

def unique(xs):
    if len(set(xs))!=len(xs):raise InputError("duplicate identity")
    return xs

def pairs(ps):
    d={}
    for k,v in ps:
        if k in d:raise InputError("duplicate JSON key")
        d[k]=v
    return d

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("snapshot",type=Path);a=p.parse_args()
    try:
        with a.snapshot.open("rb") as f:raw=f.read(2*1024*1024+1)
        if len(raw)>2*1024*1024:raise InputError("snapshot exceeds2 MiB")
        d=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(InputError("nonfinite JSON")))
        result=analyze(d);print(json.dumps(result,sort_keys=True,ensure_ascii=True));return 1 if result.get("findings") else 0
    except (InputError,ValueError,TypeError,KeyError,OSError,RecursionError) as e:
        print(json.dumps({"error":str(e)}),file=sys.stderr);return 2

def ident(x,n):
    if not isinstance(x,str) or not re.fullmatch("[0-9a-f]{"+str(n)+"}",x) or int(x,16)==0:raise InputError("invalid nonzero lowercase hex trace/span id")
    return x

def analyze(d):
    obj(d,["spans"]);nodes={};findings=[];notes=[]
    for s in arr(d["spans"]):
        obj(s,["trace_id","span_id","parent_span_id","start_ns","end_ns","service"])
        key=(ident(s["trace_id"],32),ident(s["span_id"],16))
        if key in nodes:raise InputError("duplicate trace/span identity")
        if s["parent_span_id"] is not None:ident(s["parent_span_id"],16)
        integer(s["start_ns"]);integer(s["end_ns"]);text(s["service"])
        if s["start_ns"]>s["end_ns"]:raise InputError("span ends before start")
        nodes[key]=s
    children={k:[] for k in nodes};missing=[]
    for k,s in nodes.items():
        if s["parent_span_id"] is None:continue
        parent=(k[0],s["parent_span_id"])
        if parent not in nodes:missing.append({"trace_id":k[0],"span_id":k[1],"parent_span_id":parent[1]});continue
        children[parent].append(k);p=nodes[parent]
        if s["start_ns"]<p["start_ns"] or s["end_ns"]>p["end_ns"]:notes.append({"trace_id":k[0],"span_id":k[1],"kind":"outside_observed_parent_interval","interpretation":"clock skew, asynchronous lifetime or instrumentation may explain this; not an invalid span solely for this reason"})
    cycles=set()
    for key in sorted(nodes):
        path=[];seen={};cur=key
        while cur in nodes:
            if cur in seen:
                cycle=path[seen[cur]:];cycles.add(tuple(sorted(cycle)));break
            seen[cur]=len(path);path.append(cur);s=nodes[cur]
            if s["parent_span_id"] is None:break
            cur=(cur[0],s["parent_span_id"])
    if missing:findings.append({"kind":"parents_not_in_capture","spans":missing,"interpretation":"capture completeness finding; remote/sampled parents may be absent"})
    for c in sorted(cycles):findings.append({"kind":"parent_cycle","members":[{"trace_id":k[0],"span_id":k[1]} for k in c]})
    coverage=[]
    for k,s in sorted(nodes.items()):
        intervals=sorted((max(s["start_ns"],nodes[c]["start_ns"]),min(s["end_ns"],nodes[c]["end_ns"])) for c in children[k])
        merged=[]
        for lo,hi in intervals:
            if lo>=hi:continue
            if merged and lo<=merged[-1][1]:merged[-1][1]=max(hi,merged[-1][1])
            else:merged.append([lo,hi])
        covered=sum(hi-lo for lo,hi in merged)
        coverage.append({"trace_id":k[0],"span_id":k[1],"duration_ns":s["end_ns"]-s["start_ns"],"clipped_direct_child_union_ns":covered,"uncovered_by_direct_children_ns":s["end_ns"]-s["start_ns"]-covered,"child_intervals":merged})
    return {"spans":coverage,"root_count":sum(s["parent_span_id"] is None for s in nodes.values()),"timeline_annotations":notes,"findings":findings,"coverage_is_timestamp_arithmetic_not_measured_self_latency":True}

if __name__ == "__main__":
    raise SystemExit(main())
