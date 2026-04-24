from pydantic import BaseModel, ConfigDict, Field

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================

class UnifiedDocument(BaseModel):
    """
    Hệ thống cần 6 trường thông tin chuẩn (document_id, source_type, author, category, content, timestamp). 
    TODO: Khai báo các trường với kiểu dữ liệu str ở dưới.
    """
    model_config = ConfigDict(str_strip_whitespace=True)

    document_id: str = Field(..., description="ID ổn định của tài liệu từ hệ nguồn.")
    source_type: str = Field(..., description="Loại nguồn dữ liệu, ví dụ PDF hoặc Video.")
    author: str = Field(..., description="Tác giả hoặc người tạo nội dung.")
    category: str = Field(..., description="Nhóm chủ đề để AI dễ lọc và truy xuất.")
    content: str = Field(..., description="Nội dung văn bản đã được làm sạch nhiễu.")
    timestamp: str = Field(..., description="Thời điểm tạo hoặc phát hành do hệ nguồn cung cấp.")
