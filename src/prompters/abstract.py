from abc import ABC, abstractmethod

# 추상 클래스: Prompter
# 모든 프롬프터 클래스는 이 클래스를 상속받아야 함
class Prompter(ABC):
    @abstractmethod
    def get_prompt(self) -> str:
        pass

    async def get_async_prompt(self) -> str:
        return self.get_prompt()