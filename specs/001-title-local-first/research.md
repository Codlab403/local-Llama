# research.md

## Decision: Project scope and key defaults
- Chosen scope: Local-first RAG MVP focusing on document ingestion, LlamaIndex ingestion,
  hybrid retrieval (lexical + vector), cross-encoder reranker, and Ollama local inference.

## Rationale
- Privacy-first and auditability are primary goals per PRD. Local-only defaults and
  citation-first answers are required.

## Resolved unknowns
- Auth: NO AUTH for MVP (single-user local). Documented as trade-off; production
  deployments SHOULD add auth.
- Retention: Keep raw uploads and logs indefinitely unless user deletes them. Enterprise
  retention policies deferred to deployment runbooks.

## Alternatives considered
- Auth approaches: local accounts (bcrypt), OS auth, or no auth. Chose no auth for a
  low-friction local developer preview.
- Retention options: time-based retention vs indefinite; indefinite chosen to prioritize
  auditability and local user control.

## Research tasks (short)
- Best practices for local Ollama deployment and model management.
- OCR pipeline options (pytesseract vs commercial OCR) and trade-offs for accuracy vs
  licensing.
- Dedupe algorithms for near-duplicate detection (SimHash/MinHash) and chunking
  strategies for very large docs.

## Output
- decisions recorded and applied to spec.md
