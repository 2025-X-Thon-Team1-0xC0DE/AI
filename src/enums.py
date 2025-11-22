from enum import Enum, IntEnum


# 문서 카테고리 정의 (오타 방지용 Enum)
class DocumentCategory(str, Enum):
    RESUME = "RESUME"  # 이력서
    REPORT = "REPORT"  # 보고서/기획서
    ESSAY = "ESSAY"  # 논문/에세이
    COVER_LETTER = "COVER_LETTER"  # 자기소개서


class FeedbackType(IntEnum):
    FEEDBACK = 1
    OUTLINE = 0
