# Candidate brief and comparison — 15 October 2026

**User:** Observability engineers inspecting a small captured trace after sampling or instrumentation changes.

**Pain and smallest capability:** Missing parents, cyclic ancestry and overlapping child intervals can make a trace view misleading; timestamp arithmetic should not be confused with measured self latency. Detect missing captured parents and cycles, merge clipped direct-child intervals without double counting, and annotate asynchronous/clock-skew-compatible lifetimes.

**Acceptance criteria:** Overlaps do not double count; clipping stays within parent duration; cycles are emitted once per component; same span id in different traces is allowed; missing parents are explicit; async lifetimes are annotated without being rejected.

**Demand evidence:** Inferred operator/developer need, not a verified customer request. Current upstream READMEs, relevant docs/code and accessible issues were inspected. Issue titles below provide context about maintenance and operational work; they are not presented as requests for this tool. No claimed competitor absence is inferred from a successful example here.

**Discovery path:** Accurate repository description/topics, a runnable captured-input example and this evidence file; discoverable by `opentelemetry` and the task-specific terms. No unsolicited outreach or activity manipulation.

## Relevant established alternatives found

Live GitHub searches used Most stars ordering; exact queries/URLs/observations are in research-provenance.json. Highest-star relevant comparable found for this bounded workflow: `SigNoz/signoz`. Broader collections, tutorials, proxies or unrelated applications in broad results were excluded by relevance; this is not an exhaustive global ranking. Focused invoice-rounding and matrix queries were sparse and broader established tools were retained transparently.

| Comparable | Stars observed | Latest push observed | Archived | API license classification |
| --- | ---: | --- | --- | --- |
| [SigNoz/signoz](https://github.com/SigNoz/signoz) | 32360 | 2026-10-15T05:59:25Z | False | NOASSERTION |
| [jaegertracing/jaeger](https://github.com/jaegertracing/jaeger) | 23297 | 2026-10-14T22:28:15Z | False | Apache-2.0 |
| [open-telemetry/opentelemetry-collector](https://github.com/open-telemetry/opentelemetry-collector) | 7660 | 2026-10-14T21:36:49Z | False | Apache-2.0 |

Observations are dated in research-provenance.json, including README blob hashes and accessible issue links. NOASSERTION means the API did not classify the license; upstream terms must be read before reuse. No upstream source was incorporated.

SigNoz is an observability platform; Jaeger provides distributed tracing with a Docker quickstart; OpenTelemetry Collector is a telemetry pipeline. This offline file contract avoids operating that infrastructure but lacks ingestion, visualization and monitoring. We do not claim those projects cannot inspect the same conditions. Official OpenTelemetry tracing specification informs identity/parent semantics; timestamp arithmetic here is a deliberately separate report.

Installation and first-use paths were inspected in current documentation, not benchmarked. These alternatives provide broader workflows, operational reliability features, docs/examples and support communities. This tool offers a bounded file/JSON contract, explicit failure modes and runnable fixtures but lacks their broader product capabilities, adoption evidence and maintenance history. Our build/install example measures only our behavior. Competitor installs, time-to-first-result, reliability and technical performance were not measured; no superiority claim or numerical performance comparison is made. Stars inform discovery, not quality or speed.

## Portfolio and candidate distinctness

TraceWeave inspects AI-agent JSONL action loops/context drift. This tool accepts typed span identifiers/times and audits ancestry/interval union, not agent behavior, risk scores or context drift. It is also distinct from RunMirror replay.

All 178 owned repository identities/descriptions and the current project index were compared. Related release-asset-matrix, table-reconcile, sqlite-rehearsal and traceweave READMEs were inspected. The five candidates have separate users/contracts: backup dependency preservation, Kafka recovery positions, tax allocation arithmetic, span ancestry/interval coverage and CI matrix inclusion provenance. They are independent tools, not renamed/forked/subdivided versions of one product. Shared JSON CLI and packaging scaffolding does not substitute for their distinct algorithms and tests.
