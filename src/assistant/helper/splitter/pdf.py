from src.app.utils.splitter.markdown import *
import pymupdf
import pymupdf4llm


class PDFPageSplitter(BaseSplitter):
    def __init__(self, images_dir: str = "data/media/images"):
        self.images_dir = images_dir
        self.markdown_splitter = MarkdownTextSplitter()

    def create_documents(self, pdf_path: str, page_numbers: int | list[int], use_page_as_image: bool = False) -> list[Document]:
        documents: list[Document] = []
        page_numbers = [page_numbers - 1] if isinstance(page_numbers, int) else [page_number - 1 for page_number in page_numbers]
        if not use_page_as_image:
            for page_number in page_numbers:
                markdown = pymupdf4llm.to_markdown(
                    pdf_path, 
                    page_chunks=True, 
                    pages=[page_number],
                    page_width=1024,
                    write_images=True, 
                    image_path=self.images_dir, 
                    image_format='png',
                    filename=f"{pdf_path.split('/')[-1].split('.')[0]}-{page_number + 1}",
                    ignore_graphics=True
                )
                text = markdown[0]['text']
                image_urls = self._extract_image_urls_(text)
                image_documents = [Document(content=image_url, metadata={"page_number": page_number + 1, "type": "image"}) for image_url in image_urls]
                documents.extend(image_documents)
                text_documents = self.markdown_splitter.create_documents(markdown_text=text)
                # Add "page_number" to text_documents metadata dict
                for text_document in text_documents:
                    pattern = r'!\[\]\((.*(?:png|jpg|jpeg|gif|webp|svg))\)'
                    text_document.content = re.sub(pattern, '', text_document.content).strip()
                    text_document.metadata["page_number"] = page_number + 1
                documents.extend(text_documents)
        else:
            doc = pymupdf.open(pdf_path)
            zoom = 2
            mat = pymupdf.Matrix(zoom, zoom)
            for page_number in page_numbers:
                # Use pymupdf to convert page into an image
                page = doc.load_page(page_number)
                pix = page.get_pixmap(matrix=mat)
                pdf_filename = pdf_path.split("/")[-1].split(".")[0]
                image_url = f"{self.images_dir}/{pdf_filename}-{page_number + 1}.png"
                pix.save(image_url)
                documents.append(Document(content=image_url, metadata={"page_number": page_number + 1, "type": "image"}))
        return documents


if __name__ == "__main__":
    pdf_splitter = PDFPageSplitter()
    documents = pdf_splitter.create_documents("data/pdfs/TPHCM - TRAVEL GUIDE (tiếng Anh).pdf", page_numbers=15)
    for document in documents:
        print(document)