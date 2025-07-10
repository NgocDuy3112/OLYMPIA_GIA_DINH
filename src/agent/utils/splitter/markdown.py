from src.app.utils.splitter.base import *



class MarkdownTextSplitter(BaseSplitter):
    def __init__(self, chunk_size: int = 4096, chunk_overlap: int = 256):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def create_documents(self, markdown_text: str) -> list[Document]:
        # Split by Markdown headers (#, ##, ###, etc.)
        chunks = re.split(r'\n(?=#)', markdown_text)
        split_docs = []

        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            if len(chunk) <= self.chunk_size:
                split_docs.append(Document(content=chunk))
            else:
                # Further split long chunks by paragraphs or lines
                split_docs.extend(self._split_large_chunk(chunk))
        return split_docs

    def _split_large_chunk(self, text: str) -> list[Document]:
        paragraphs = text.split("\n\n")
        docs = []
        current = ""
        for para in paragraphs:
            if len(current) + len(para) < self.chunk_size:
                current += para + "\n\n"
            else:
                docs.append(Document(content=current.strip(), metadata={"type": "text"}))
                # Apply overlap from end of previous
                overlap = current[-self.chunk_overlap:] if self.chunk_overlap > 0 else ""
                current = overlap + para
        if current:
            docs.append(Document(content=current.strip(), metadata={"type": "text"}))
        return docs