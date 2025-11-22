from abc import ABC, abstractmethod

class Prompter(ABC):
    @abstractmethod
    def get_prompt(self) -> str:
        pass

    async def get_async_prompt(self) -> str:
        return self.get_prompt()