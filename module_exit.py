from dotenv import load_dotenv
import os
load_dotenv()  # Loads variables from .env

openai_key = os.getenv("OPENAI_API_KEY")


from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

def exit_advisor_function(conversation_history: str) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an assistant that decides whether a job candidate conversation 
        should be ended or continued. Your job is to classify the candidate's latest message into one of three categories:
        
        - END: Candidate clearly confirmed an interview time, or declined the role. 
        - SCHEDULING: Candidate suggested a date or time (even partial, like just a date).
        - CONTINUE: Candidate is still engaged in discussion or undecided.
        """),
        ("human", """Examples:

        Candidate: I already accepted another offer.
        Response: END (Candidate is no longer available)

        Candidate: I'm not looking for a job right now.
        Response: END (Candidate declined)

        Candidate: Can you tell me more about the role?
        Response: CONTINUE (Still engaged)

        Candidate: I'm interested but need to check my schedule.
        Response: CONTINUE (Still considering)

        Candidate: August 7th at 2:00 PM is great.
        Response: END (Confirmed interview time)

        Candidate: Wednesday at 10:00 AM works for me.
        Response: END (Confirmed interview time)

        Candidate: How about September 24 around 14:00?
        Response: SCHEDULING (Candidate proposed a time, need to check availability)

        Candidate: How about September 24?
        Response: SCHEDULING (Candidate proposed a date, need to check available times)

        Now classify the following message:
        """),
        ("human", conversation_history)
    ])

    response = llm(prompt.format_messages())
    content = response.content.lower()

    should_end = "yes" in content
    return {
        "should_end": should_end,
        "explanation": response.content.strip()
    }


