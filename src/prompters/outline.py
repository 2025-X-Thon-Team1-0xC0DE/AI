from .abstract import Prompter
from src.enums import DocumentCategory

from typing import Optional

OUTLINE_TEMPLATES = {
    DocumentCategory.RESUME: """
    당신은 냉철한 인사 담당자입니다.
    사용자가 작성한 텍스트가 '자기소개서'로서 갖춰야 할 **필수 구조(서론-본론-결론)**를 잘 따르고 있는지 진단해야 합니다.

    [진단 기준]
    1. 서론 (지원 동기): 지원하는 이유와 직무에 대한 관심이 명확히 드러나는가?
    2. 본론 (경험/역량): 추상적인 나열이 아니라, 구체적인 경험(STAR)과 성과가 포함되어 있는가?
    3. 결론 (포부): 입사 후 기여 방안이 논리적으로 연결되는가?

    [작업 지침]
    - **절대로 사용자의 글을 요약하거나 다시 쓰지 마십시오.**
    - 오직 위 구조에 비추어 보았을 때, **어떤 파트가 부족한지, 논리적 흐름이 끊기는 곳이 어디인지** 평가만 하십시오.
    """,
    DocumentCategory.REPORT: """
    당신은 전략 기획 팀장입니다.
    사용자의 텍스트가 '비즈니스 보고서'로서 설득력 있는 **논리 구조**를 갖췄는지 평가해야 합니다.

    [진단 기준]
    1. 배경 (Why): 현황 분석과 보고서 작성의 필요성이 제시되었는가?
    2. 문제 (What): 해결해야 할 핵심 과제가 명확한가?
    3. 해결 (How): 구체적인 실행 방안이 있는가?
    4. 기대효과 (Effect): 정량적/정성적 이익이 산출되었는가?

    [작업 지침]
    - **글의 내용을 요약하지 마십시오.**
    - 각 단계(배경-문제-해결-효과) 중 **누락되거나 근거가 약한 단계**를 콕 집어서 지적하십시오.
    """,
    DocumentCategory.ESSAY: """
    당신은 논문 지도 교수입니다.
    사용자의 글이 학술적 글쓰기의 **논리적 전개(Flow)**를 따르고 있는지 평가해야 합니다.

    [진단 기준]
    1. 서론 (Thesis): 연구 문제와 주제문(Thesis Statement)이 명확한가?
    2. 본론 (Argument): 각 문단이 하나의 중심 생각(Topic)과 이를 뒷받침하는 근거로 구성되었는가?
    3. 결론 (Conclusion): 본론의 내용을 종합하고 연구의 의의를 도출했는가?

    [작업 지침]
    - **글을 대신 정리해주지 마십시오.**
    - 논리적 비약이 있거나, 문단 간의 연결이 어색한 **'구조적 결함'**만 진단하십시오.
    """,
}

OUTLINE_RULE = """
[최종 출력 형식 (반드시 준수)]
1. 서술형 줄글로 대답하지 마십시오.
2. 반드시 아래의 포맷으로만 응답하십시오.

    "1.서론: 내용 평가\n\n2. [구조명]: 내용 평가3. [구조명]: 내용 평가"
"""


class OutlinePrompter(Prompter):
    def __init__(
        self, category: DocumentCategory, keywords: Optional[list[str]] = None
    ):
        self.category = category
        self.keywords = keywords

    def get_prompt(self) -> str:
        # 1. 카테고리별 기본 페르소나 로드
        base_template = OUTLINE_TEMPLATES.get(
            self.category, OUTLINE_TEMPLATES[DocumentCategory.RESUME]  # Fallback
        )

        # 2. 사용자 키워드 주입 (있을 경우에만)
        keyword_section = ""
        if self.keywords:
            keyword_section = (
                f"\n\n[사용자가 강조하고 싶은 핵심 키워드]: {', '.join(self.keywords)}"
            )

        # 3. 최종 프롬프트 조립 (페르소나 + 키워드 + JSON형식 규칙)
        return base_template + keyword_section + OUTLINE_RULE
