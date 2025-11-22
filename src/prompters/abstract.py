from abc import ABC, abstractmethod

# 공통 규칙
COMMON_RULE = "\n\n중요: 사용자의 글을 절대 직접 수정하지 마세요. 대신 '이 부분은 ~한 이유로 어색함', '~에 대한 검증이 부족함' 등의 형식으로 가이드만 제시하세요."

# 추상 클래스: Prompter
# 모든 프롬프터 클래스는 이 클래스를 상속받아야 함
class Prompter(ABC):
    @abstractmethod
    def get_prompt(self) -> str:
        pass

    async def get_async_prompt(self) -> str:
        return self.get_prompt()