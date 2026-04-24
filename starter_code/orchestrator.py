import glob
import json
import os

from process_unstructured import process_pdf_data, process_video_data
from quality_check import run_semantic_checks
from schema import UnifiedDocument

# ==========================================
# ROLE 4: DEVOPS & INTEGRATION SPECIALIST
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, "..", "raw_data")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "processed_knowledge_base.json")


def _process_and_validate(raw_data: dict, processor) -> dict | None:
    processed_doc = processor(raw_data)
    validated_doc = UnifiedDocument(**processed_doc).model_dump()
    if run_semantic_checks(validated_doc):
        return validated_doc
    return None


def run_pipeline():
    final_kb = []

    pdf_files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "group_a_pdfs", "*.json")))
    for file_path in pdf_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        validated_doc = _process_and_validate(raw_data, process_pdf_data)
        if validated_doc is not None:
            final_kb.append(validated_doc)

    video_files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "group_b_videos", "*.json")))
    for file_path in video_files:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        validated_doc = _process_and_validate(raw_data, process_video_data)
        if validated_doc is not None:
            final_kb.append(validated_doc)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_kb, f, indent=4, ensure_ascii=False)

    print(f"Pipeline finished! Saved {len(final_kb)} records.")


if __name__ == "__main__":
    run_pipeline()
