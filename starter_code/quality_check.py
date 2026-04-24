# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================

def run_semantic_checks(doc_dict: dict) -> bool:
    required_fields = (
        "document_id",
        "source_type",
        "author",
        "category",
        "content",
        "timestamp",
    )
    for field in required_fields:
        value = str(doc_dict.get(field, "") or "").strip()
        if not value:
            return False

    content = str(doc_dict.get("content", "") or "").strip()

    # 1. Reject empty or too-short content.
    if len(content) < 10:
        return False

    # 2. Reject records that still contain obvious extraction/runtime errors.
    toxic_keywords = ["Null pointer exception", "OCR Error", "Traceback"]
    normalized_content = content.lower()
    for keyword in toxic_keywords:
        if keyword.lower() in normalized_content:
            return False

    return True
