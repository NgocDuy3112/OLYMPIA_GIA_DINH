from abc import ABC, abstractmethod
import re
from src.app.schema.document import Document


class BaseSplitter(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def create_documents(self, **kwargs) -> list[Document]:
        pass

    def _chunk_text_by_sentences_(self, text: str) -> list[str]:
        sentences = re.split(r'(?<=[\.\!\?\。！？])\s+|\n+', text)
        chunks = []
        current_chunk = []
        current_length = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            sentence_length = len(sentence)
            if current_length + sentence_length > self.chunk_size:
                chunk = ' '.join(current_chunk).strip()
                if chunk:
                    chunks.append(chunk)
                overlap_text = ' '.join(current_chunk)[-self.chunk_overlap:]
                current_chunk = [overlap_text, sentence] if overlap_text else [sentence]
                current_length = len(' '.join(current_chunk))
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        if current_chunk:
            chunks.append(' '.join(current_chunk).strip())
        return chunks

    def _chunk_text_by_paragraphs_(self, text: str) -> list[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        current_chunk = []
        current_length = 0
        for paragraph in paragraphs:
            paragraph_len = len(paragraph)
            if current_length + paragraph_len > self.chunk_size:
                # Finalize current chunk
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                # Apply paragraph-based overlap (not exact char overlap)
                if self.chunk_overlap > 0:
                    overlap_text = "\n\n".join(current_chunk)[-self.chunk_overlap:]
                    overlap_paragraphs = [p.strip() for p in overlap_text.split("\n\n") if p.strip()]
                    current_chunk = overlap_paragraphs
                    current_length = sum(len(p) for p in current_chunk)
                else:
                    current_chunk = []
                    current_length = 0
            current_chunk.append(paragraph)
            current_length += paragraph_len
        if current_chunk:
            chunks.append("\n\n".join(current_chunk))
        return chunks

    def _extract_image_urls_(self, text: str) -> list[str]:
        # Match Markdown or HTML style links and images
        return re.findall(r'!\[\]\((.*(?:png|jpg|jpeg|gif|webp|svg))\)', text)