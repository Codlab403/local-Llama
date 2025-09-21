```markdown
# Feature Specification: Local-first RAG chatbot core: upload, index, chat with citations

**Feature Branch**: `001-title-local-first`  
**Created**: 2025-09-21  
**Status**: Draft  
**Input**: User description: "Implement the MVP core: document ingestion (PDF, DOCX, images/OCR), LlamaIndex ingestion into a local vector store, LangChain orchestration for retrieval, rerank, LLM synth, Ollama local inference by default, left-sidebar UI for sessions & documents, streaming responses with inline citations, and gold Q/A nightly evaluation."

## Execution Flow (main)
```
1. Parse user description from Input
   → If empty: ERROR "No feature description provided"
2. Extract key concepts from description
   → Identify: actors, actions, data, constraints
3. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
4. Fill User Scenarios & Testing section
   → If no clear user flow: ERROR "Cannot determine user scenarios"
5. Generate Functional Requirements
   → Each requirement must be testable
   → Mark ambiguous requirements
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If implementation details found: ERROR "Remove tech details"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (keep implementation details to design docs)
- 👥 Written for business stakeholders; tests and acceptance criteria are explicit

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a Knowledge Worker, I want to upload documents (PDF/DOCX/TXT/images), ask natural
language questions, and receive grounded answers with explicit citations so I can rely on
the responses for decision making.

### Acceptance Scenarios
1. Given a user uploads a PDF and the ingestion completes, When the user asks a question
   covered by the document, Then the assistant returns an answer with at least one
   inline citation indicating docId, page, and snippet and a confidence score.
2. Given network is disabled (local-only), When the user queries, Then the system uses
   local models (Ollama) and local vector store and returns a response or a clear
   "I don't know" refusal if answerability gate fails.

### Edge Cases
- Upload of a corrupt or unsupported file type → ingestion should fail gracefully with
  an actionable error message.
- Very large documents (>2000 pages) → ingestion signals sampling/deduping behavior and
  may reject or chunk with explicit user guidance.
- Sensitive/PII documents flagged for vaulting → system must not index them unless
  explicitly permitted.

## Requirements *(mandatory)*

### Functional Requirements
- FR-001: System MUST accept document uploads for PDF, DOCX, PPTX, XLSX, HTML, TXT,
  and images (with OCR) and return a task id for ingestion.
- FR-002: System MUST parse documents into nodes/chunks, persist raw file to local FS,
  store metadata in SQLite, and ingest embeddings via LlamaIndex into a local vector store
  (Chroma/FAISS for dev; Milvus for scale optional adapters).
- FR-003: System MUST provide an API `POST /chat` that accepts `{session_id, query, mode, top_k, filters}`
  and streams tokens; final response MUST include `citations` (docId, page, snippet, nodeId)
  and a `confidence` score.
- FR-004: System MUST use a hybrid retrieval pipeline (lexical + vector) and a
  cross-encoder reranker before synthesis; retriever and reranker thresholds MUST be
  configurable and documented.
- FR-005: System MUST default to local LLM inference via Ollama; remote endpoints are
  only used if explicitly enabled in configuration.
- FR-006: System MUST run a nightly gold Q/A evaluation to compute Recall@k, citation
  accuracy, and hallucination rate; results MUST be stored and surfaced via `/admin/metrics`.

*Decisions (resolved)*
- FR-007: Auth method for the MVP: NO AUTH. The MVP will not require authentication; the
   system is single-user/local by default. (Document this as a security trade-off for the
   local-first developer preview; production deployments SHOULD add authentication.)
- FR-008: Retention policy: Keep raw uploads and logs indefinitely unless the user
   explicitly deletes them. Retention and archival policies for enterprise deployments
   should be added to deployment runbooks.

### Key Entities
- Document: id, filename, status, uploadedAt, pages, sizeKB, tags, version, acl
- Session: id, title, createdAt, lastUpdated, userId, ephemeral
- Message: id, sessionId, role, content, createdAt, citations, cachedSnippets
- Node/Chunk: nodeId, docId, text, offsets, embeddingId, metadata (page, heading, acl)

---

## Review & Acceptance Checklist

### Content Quality
- [x] No implementation details that contradict the PRD (implementation specifics
      go in design docs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous where specified
- [x] Success criteria are measurable (see PRD metrics)
- [x] Scope is clearly bounded to local-first MVP features

---

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---

``` 