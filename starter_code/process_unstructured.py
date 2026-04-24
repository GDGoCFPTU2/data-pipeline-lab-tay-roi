import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================

PDF_NOISE_PATTERN = re.compile(r"(HEADER_PAGE_\d+|FOOTER_PAGE_\d+)")
VIDEO_NOISE_PATTERN = re.compile(r"\[[^\]]+\]")


def _first_value(raw_json: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        value = raw_json.get(key)
        if value is not None:
            return str(value)
    return default


def _normalize_scalar(value: str, fallback: str) -> str:
    normalized = re.sub(r"\s+", " ", str(value)).strip()
    return normalized or fallback


def _normalize_content(value: str) -> str:
    lines = [line.strip() for line in str(value).splitlines() if line.strip()]
    return "\n".join(lines).strip()


def _build_unified_document(
    *,
    document_id: str,
    source_type: str,
    author: str,
    category: str,
    content: str,
    timestamp: str,
) -> dict:
    return {
        "document_id": _normalize_scalar(document_id, "unknown-document"),
        "source_type": source_type,
        "author": _normalize_scalar(author, "Unknown"),
        "category": _normalize_scalar(category, "Uncategorized"),
        "content": _normalize_content(content),
        "timestamp": _normalize_scalar(timestamp, "Unknown"),
    }

def process_pdf_data(raw_json: dict) -> dict:
    # Bước 1: Làm sạch nhiễu (Header/Footer) khỏi văn bản
    raw_text = _first_value(raw_json, "extractedText", "content")
    # Loại bỏ token header/footer do OCR chèn vào.
    cleaned_content = PDF_NOISE_PATTERN.sub("", raw_text)
    cleaned_content = _normalize_content(cleaned_content)
    
    # Bước 2: Map dữ liệu thô sang định dạng chuẩn của UnifiedDocument
    return _build_unified_document(
        document_id=_first_value(raw_json, "docId", "document_id"),
        source_type="PDF",
        author=_first_value(raw_json, "authorName", "author", default="Unknown"),
        category=_first_value(raw_json, "docCategory", "category", default="Uncategorized"),
        content=cleaned_content,
        timestamp=_first_value(raw_json, "createdAt", "timestamp", default="Unknown"),
    )

def process_video_data(raw_json: dict) -> dict:
    raw_transcript = _first_value(raw_json, "transcript", "content")
    cleaned_transcript = VIDEO_NOISE_PATTERN.sub("", raw_transcript)
    cleaned_transcript = _normalize_content(cleaned_transcript)

    # Map dữ liệu thô từ Video sang định dạng chuẩn giống UnifiedDocument.
    return _build_unified_document(
        document_id=_first_value(raw_json, "video_id", "document_id"),
        source_type="Video",
        author=_first_value(raw_json, "creator_name", "author", default="Unknown"),
        category=_first_value(raw_json, "category", "docCategory", default="Uncategorized"),
        content=cleaned_transcript,
        timestamp=_first_value(
            raw_json,
            "published_timestamp",
            "createdAt",
            "timestamp",
            default="Unknown",
        ),
    )
