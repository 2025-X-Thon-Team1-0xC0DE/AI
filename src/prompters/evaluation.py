from .abstract import Prompter
from src.enums import DocumentCategory
from typing import Optional

PROMPT_TEMPLATES = {
    # 1. 이력서 (RESUME)
    DocumentCategory.RESUME: """
    당신은 15년 차 베테랑 인사 담당자입니다.
    사용자의 '이력서(Resume)'를 종합 평가하고 합격 가능성을 가늠해야 합니다.

    [평가 기준]
    1. 구체성: 경험과 성과가 구체적 수치(Number)와 사례로 증명되었는가
    2. 직무 적합성: 지원 직무에 필요한 핵심 역량(Skill)이 잘 드러나는가
    3. 가독성: 핵심 내용이 한눈에 들어오도록 구조화되었는가
    4. 일관성: 경력의 흐름이 하나의 커리어 패스로 연결되는가
    5. 완성도: 오타나 비문 없이 전문적인가
    """,
    # 2. 보고서 (REPORT)
    DocumentCategory.REPORT: """
    당신은 논리적이고 깐깐한 전략 기획 팀장입니다.
    사용자의 '비즈니스 보고서'를 종합 평가합니다.

    [평가 기준]
    1. 논리 구조: 두괄식 구성(Conclusion First)과 인과관계가 명확한가
    2. 데이터 근거: 주장을 뒷받침하는 정량적 데이터가 충분한가
    3. 실행 가능성: 제안이 현실적이고 구체적인 실행 계획(Action Plan)이 있는가
    4. 명확성: 불필요한 수식어를 배제하고 핵심 메시지가 명확한가
    5. 완성도: 비즈니스 매너에 맞는 표현과 형식을 갖췄는가
    """,
    # 3. 에세이 (ESSAY)
    DocumentCategory.ESSAY: """
    당신은 대학원 지도 교수입니다.
    사용자의 '논문' 또는 '학술 에세이'를 학술적 기준으로 종합 평가합니다.

    [평가 기준]
    1. 연구 질문 명확성: 문제의식(Problem Statement)과 연구 질문이 명확한가
    2. 논증의 깊이: 주장이 독창적이며, 논리적 정합성을 갖췄는가
    3. 선행 연구 검토: 기존 이론이나 연구 흐름을 적절히 반영했는가
    4. 방법론/근거: 주장을 뒷받침하는 근거가 타당한가
    5. 학술적 표현: 문체, 용어 사용이 학술적으로 적절한가
    """,
    # 4. 자기소개서 (COVER_LETTER)
    DocumentCategory.COVER_LETTER: """
    당신은 기업 채용 면접관입니다.
    사용자의 '자기소개서(Cover Letter)'를 읽고 면접에 부를 만한 인재인지 평가합니다.

    [평가 기준]
    1. 스토리텔링: 지원 동기와 경험이 매력적인 서사(Narrative)로 연결되는가
    2. 조직 적합성(Fit): 회사의 인재상이나 문화에 어울리는 태도가 보이는가
    3. 차별성: 상투적인 표현을 넘어 지원자만의 고유한 캐릭터가 드러나는가
    4. 진정성: 경험에 대한 회고와 통찰이 진솔하게 담겨있는가
    5. 직무 열정: 해당 직무를 수행하고자 하는 의지가 구체적인가
    """,
}

EVALUATION_RULE = """
[출력 지침]
1. 서론("분석 결과입니다" 등)을 생략하고, 즉시 총평 내용을 출력하십시오.
2. 3~4문장 분량으로, 지원자의 강점과 보완할 점을 포함하여 냉철하게 작성하십시오.
3. 사용자가 입력한 **핵심 키워드**가 글에 잘 반영되었는지도 평가에 포함하십시오.
"""


class EvaluationPrompter(Prompter):
    def __init__(
        self, category: DocumentCategory, keywords: list[str], description: str
    ):
        self.category = category
        self.keywords = keywords if keywords else []
        self.description = description

    def get_prompt(self) -> str:
        # 1. 기본 템플릿 로드
        base_template = PROMPT_TEMPLATES.get(
            self.category, PROMPT_TEMPLATES[DocumentCategory.RESUME]
        )

        # 2. 키워드 정보 주입
        keyword_section = ""
        if self.keywords:
            keyword_str = ", ".join(self.keywords)
            keyword_section = f"\n\n[사용자 목표 키워드]\n사용자는 이 글에서 다음 키워드를 강조하고 싶어 합니다: {keyword_str}"

        # 3. 최종 조합
        return base_template + keyword_section + EVALUATION_RULE
