from dotenv import load_dotenv
import os
load_dotenv()  # Loads variables from .env
openai_key = os.getenv("OPENAI_API_KEY")


from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4", temperature=0.2)

def prepare_job_description_retriever(pdf_path: str, persist_dir: str, openai_key: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    embedding = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_key)# צור embeddings
    db = Chroma.from_documents(documents, embedding, persist_directory=persist_dir)# צור vector store עם Chroma
    return db.as_retriever()# צור רטריבר


retriever = prepare_job_description_retriever(
    pdf_path="Python Developer Job Description.pdf",
    persist_dir="./chroma_store",
    openai_key=openai_key
    )

def info_advisor_fun_ction(candidate_message: str,retriever=retriever) -> str:
     job_description_context = retriever.get_relevant_documents(candidate_message)
     job_description_text = "\n".join([doc.page_content for doc in job_description_context])
     prompt = ChatPromptTemplate.from_messages([
        ("system",
         f"""You are an assistant that evaluates whether a candidate meets at least two job requirements based on the conversation history and the following job description:
         {job_description_text}
         Return your response in the following format:
         schedule: yes/no
         required qualifications: <list of job requirements>
         additional relevant information: <answer to candidate's question, if any>
         If the candidate meets at least two requirements, set schedule: yes.
         If not, set schedule: no.
         list all the job requirements under 'required qualifications'.
         If the candidate asked a question, include a helpful answer in 'additional relevant information'.
         If not, leave that field empty.
         """),
        ("human", f"""Candidate message: "{candidate_message}"
         Respond according to the format above.
         """)
         ])
     response = llm.invoke(prompt.format_messages()) 
     content = response.content.strip().lower()
     lines = content.splitlines()
     result = {
        "schedule": None,
        "required_qualifications": "",
        "additional_relevant_information": ""
        }
     for line in lines:
        if line.lower().startswith("schedule:"):
            result["schedule"] = line.split(":", 1)[1].strip().lower()
        elif line.lower().startswith("required qualifications:"):
            result["required_qualifications"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("additional relevant information:"):
            result["additional_relevant_information"] = line.split(":", 1)[1].strip()
     return result


info_advisor_fun_ction ("i have 3 years experience in python, is the job hybrid?",retriever)




