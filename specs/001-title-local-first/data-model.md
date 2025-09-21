# data-model.md

## Entities

### Document
- id: uuid
- filename: string
- status: enum(indexing|ready|error|queued)
- uploadedAt: timestamp
- pages: integer
- sizeKB: integer
- tags: array[string]
- version: integer
- acl: array[string]

Validation:
- filename required
- pages >= 0

### Session
- id: uuid
- title: string
- createdAt: timestamp
- lastUpdated: timestamp
- userId: string | null
- ephemeral: boolean

### Message
- id: uuid
- sessionId: uuid
- role: enum(user|assistant)
- content: string
- createdAt: timestamp
- citations: array[{docId, page, snippet, nodeId, status}]
- cachedSnippets: map(docId -> short text)

### Node/Chunk
- nodeId: string
- docId: uuid
- text: string
- startOffset: integer
- endOffset: integer
- embeddingId: string
- metadata: object {page, heading, acl}

## Relationships
- Document 1..* -> Node/Chunk
- Session 1..* -> Message
- Message 0..* -> Citation -> Document/Node

## Sample JSON schema (Document)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "id": {"type":"string"},
    "filename": {"type":"string"},
    "status": {"type":"string"},
    "uploadedAt": {"type":"string","format":"date-time"}
  },
  "required": ["id","filename","status","uploadedAt"]
}
```
