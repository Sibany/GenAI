import chromadb
from chromadb.config import Settings
from PyPDF2 import PdfReader

reader = PdfReader("Python Developer Job Description.pdf")

text = ""
for page in reader.pages:
    text += page.extract_text()

client = chromadb.PersistentClient(path="my_chroma_db", settings=Settings())
collection = client.get_or_create_collection(name="pdf_collection")

collection.add(
    documents=[text],
    ids=["pdf1"],
    metadatas=[{"source": "example.pdf"}]
)