from dotenv import load_dotenv
import os
load_dotenv()  # Loads variables from .env

openai_key = os.getenv("OPENAI_API_KEY")

#print(openai_key[:5])  # Just to check, don't print the full key!


from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)

def exit_advisor_function(conversation_history: str) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that decides whether a job candidate conversation should be ended."),
        ("human", """Here are some examples:

            Candidate: I already accepted another offer.
            Response: Yes, the candidate is no longer available. End the conversation.

            Candidate: I'm not looking for a job right now.
            Response: Yes, the candidate is not interested. End the conversation.

            Candidate: Can you tell me more about the role?
            Response: No, the candidate is still engaged. Continue the conversation.

            Candidate: I'm interested but need to check my schedule.
            Response: No, the candidate is considering. Continue the conversation.
                    
            Candidate:  august 7th at 2:00 PM is great.
            Response: Yes, the candidate has scheduled an interview. End the conversation. 

            Candidate:  Wednesday at 10:00 AM works for me..
            Response: Yes, the candidate has scheduled an interview. End the conversation.        

            Now evaluate the following message:
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


