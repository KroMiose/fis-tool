# src/chat_models/base.py
from abc import ABC, abstractmethod
from typing import Generator


class Chatbot(ABC):

    @abstractmethod
    def ask_question(self, question: str) -> Generator[str, None, None]:
        pass
