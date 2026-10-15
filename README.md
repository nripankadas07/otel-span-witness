# otel-span-witness

Detect missing captured parents and cycles, merge clipped direct-child intervals without double counting, and annotate asynchronous/clock-skew-compatible lifetimes.

## User and task

Observability engineers inspecting a small captured trace after sampling or instrumentation changes. Missing parents, cyclic ancestry and overlapping child intervals can make a trace view misleading; timestamp arithmetic should not be confused with measured self latency.

## Install and first useful result

Python 3.10+ and pip. Git source install; no external-registry release is claimed.

```sh
git clone https://github.com/nripankadas07/otel-span-witness.git
cd otel-span-witness
python -m venv .venv
# POSIX: . .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install .
otel-span-witness example.json
```

The root interval[0,100] has overlapping direct children[10,60] and[40,80]. Their clipped union is 70 ns, not 90 ns; uncovered arithmetic is 30 ns. The example is synthetic. JSON goes to stdout. Exit0 means analyzed with no review findings; exit 1 means review findings; exit 2 means malformed/unsupported input or an IO error. Differences explicitly labeled informational do not alone trigger exit 1. Help: `otel-span-witness --help`.

## Input contract

Top-level spans array. Each record requires trace_id (32 lowercase nonzero hex digits), span_id (16), parent_span_id (16 or null), start_ns, end_ns and service. Identity is(trace_id,span_id). Parent lookup stays within the same trace. Nanosecond times are nonnegative signed64-bit and end>=start. Duplicate identities fail. Missing parents are capture-completeness findings, not proof of invalid instrumentation. Parent cycles are findings. Child intervals are clipped to the observed parent and unioned; uncovered time is arithmetic only. Children extending beyond parent intervals are informational annotations, not automatic failures.

Every object rejects unknown keys. CLI input is UTF-8 JSON, read with a 2 MiB cap before parsing; duplicate keys/nonfinite values fail. Default arrays allow at most 512 entries, strings1..256 characters and nonnegative integers up to2^63-1 except where a tighter/different bound is documented. The example shows the complete input shape. JSON output includes the supplied identities; review it before sharing sensitive inputs.

## Validate

```sh
python -m unittest -v
python -m compileall -q otel_span_witness.py
python -m pip wheel --no-deps --wheel-dir dist .
python -m venv /tmp/otel-span-witness-installed
/tmp/otel-span-witness-installed/bin/python -m pip install --no-index --no-deps dist/*.whl
python test_installed_cli.py /tmp/otel-span-witness-installed/bin/python
```

The last commands show the Linux/POSIX path; use the equivalent Scripts/python.exe path on Windows. Remote configured CI uses Linux Python 3.10/3.12/3.14. [Validation](VALIDATION.md) records actual preparation checks and limits; a workflow configuration is not itself proof of a passing run.

## Scope and limitations

Simplified explicit JSON contract, not an OTLP/protobuf/Jaeger importer. No collector, remote lookup, span-link/event analysis, clock synchronization or semantic-convention validation. Absent sampled/remote parents may be legitimate. Child coverage is not CPU time or measured self latency; cross-service clocks may differ. No production trace is sent anywhere.

No runtime third-party packages. Setuptools is a build dependency. Original implementation developed with AI assistance, MIT licensed; no competitor code, prose or branding copied. [Research](RESEARCH.md), [contribution](CONTRIBUTING.md), [support](SUPPORT.md) and [security](SECURITY.md) guidance are included.
