```markdown
<!--
Sync Impact Report
- Version change: 2.1.1 → 2.2.0
- Modified principles: added project-specific principles (Privacy-First Local Operation,
	Citation-First Answers), clarified Test-First requirement and Observability defaults
- Added sections: Deployment & Security Constraints; Release & Versioning Policy
- Removed placeholder tokens and synchronized templates: plan-template.md, spec-template.md,
	tasks-template.md reviewed (see checklist below)
- Templates requiring updates:
	- .specify/templates/plan-template.md ✅ reviewed (no edits required)
	- .specify/templates/spec-template.md ✅ reviewed (no edits required)
	- .specify/templates/tasks-template.md ✅ reviewed (no edits required)
- Follow-up TODOs:
	- RATIFICATION_DATE intentionally left TODO (unknown) — add actual ratification date when
		the constitution is formally adopted.
-->

# Local Document / Knowledge-Base Chatbot Constitution

## Core Principles

### I. Privacy-First Local Operation
All default configurations MUST prioritize local-only operation and data residency. Network
access to external LLMs or telemetry endpoints is allowed only when explicitly enabled and
documented. Rationale: the project is designed to run in air-gapped or privacy-sensitive
environments (see PRD — Local-first RAG). This is a non-negotiable default for builds
targeting on-prem or local deployments.

### II. Traceable, Citation-First Answers
All assistant outputs that reference documents MUST include explicit citations (docId, page,
snippet or nodeId) and an auditable trace of retrieval and reranker scores. Rationale: the
product's core value is auditable, grounded answers with low hallucination as stated in the
PRD.

### III. Test-First & Nightly Evaluation
Tests (unit, integration, contract) MUST be written before implementation for new features
(TDD where practical). A gold Q/A evaluation suite MUST run nightly to monitor recall,
citation accuracy, and hallucination metrics. Rationale: continuous measurement is required
to meet success metrics (Recall@10, citation accuracy).

### IV. Hybrid Retrieval & Re-rank Discipline
Retrieval flows MUST combine lexical filters (e.g., FTS5/metadata filters) with vector
retrieval and a cross-encoder reranker for top-K candidates. All retriever/reranker choices
and thresholds MUST be documented in design docs. Rationale: hybrid strategies reduce
hallucination and improve citation quality.

### V. Observability & Minimal Telemetry by Default
Instrumentation (LangSmith traces or equivalent) MUST emit enough data to reconstruct
retrieval chains, reranker scores, LLM latencies, and final outputs for audits. Telemetry to
external services is DISABLED by default; enabling requires explicit configuration and
justification. Rationale: balances observability and privacy.

## Deployment & Security Constraints

### Deployment Constraints
Services MUST bind to localhost by default. Bundled installers or Docker images for local
deployments MUST document how to opt into networked, multi-node, or hosted-LLM modes.

### Data Protection and PII
PII detection and optional redaction at ingestion time MUST be supported and clearly
configurable. Sensitive documents MAY be vaulted (not indexed) if requested.

## Development Workflow & Quality Gates

### Review & Testing Requirements
- All PRs that add or change retrieval, indexing, or LLM prompting MUST include contract
	tests that assert retrieval behavior and citation presence.
- Changes to system prompts or answerability gates MUST include regression tests against
	the gold Q/A set or a clearly documented rationale and risk assessment.

### Release & Versioning Policy
We use semantic versioning for the constitution itself. MAJOR for incompatible governance
changes; MINOR for added/expanded principles or sections; PATCH for wording, typos, or
non-semantic clarifications. Implementation artifacts should follow conventional semantic
versioning per component (e.g., backend API, vector DB adapter).

## Governance
Amendments to this constitution MUST be recorded in the document history, include a
justification and migration plan for breaking changes, and be communicated to the team. For
non-trivial changes (MAJOR), a two-step approval (design review + governance sign-off) is
required. For MINOR/PATCH changes, a single documented review and an automated tests run
are sufficient.

All feature plans (e.g., files created from `/plan`) MUST include a "Constitution Check"
section derived from this file; failing checks require documented complexity exceptions.

**Version**: 2.2.0 | **Ratified**: TODO(RATIFICATION_DATE): unknown | **Last Amended**: 2025-09-21
```