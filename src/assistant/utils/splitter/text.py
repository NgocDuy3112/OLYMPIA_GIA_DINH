from src.app.utils.splitter.base import *


class TextSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 2048, chunk_overlap: int = 32, **kwargs):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def create_documents(self, text: str, by_paragraph: bool = False) -> list[Document]:
        chunks = self._chunk_text_by_sentences_(text) if by_paragraph is False else self._chunk_text_by_paragraphs_(text)
        return [Document(page_content=chunk, metadata={"type": "text"}) for chunk in chunks]