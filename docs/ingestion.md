# Ingestion

The ingestion layer turns raw source material into graph and vector-ready knowledge.

## Supported Inputs

- PDF
- DOCX
- PPTX
- Images
- Audio
- Video
- SQL data
- REST APIs
- Web pages
- SharePoint
- Confluence
- Google Drive

## Pipeline

```text
Source connector
→ parser
→ OCR or VLM extraction
→ chunking
→ metadata enrichment
→ PII detection
→ entity extraction
→ relationship extraction
→ claim extraction
→ triple extraction
→ embedding generation
→ graph indexing
→ vector indexing
```

## Chunking Strategy

Start with overlapping semantic chunking, then add:

- layout-aware chunking
- table-aware chunking
- heading-aware chunking
- multimodal chunking

## Metadata

Each document and chunk should include:

- source ID
- document ID
- chunk ID
- file name
- page number where available
- section heading where available
- ingestion timestamp
- classification
- allowed roles
- parser used
- confidence scores
