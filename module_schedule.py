
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from typing import List, Dict
import sql


load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Mock function to simulate available slots
def mock_query_available_slots(preferred_date: str) -> List[str]:
    return [
        f"{preferred_date} 10:00",
        f"{preferred_date} 14:00",
        f"{preferred_date} 16:00"
    ]

# Fallback slot logic
def fallback_slots(start_date: str) -> List[str]:
    for i in range(1, 7):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
        slots = mock_query_available_slots(date)
        if slots:
            return slots
    return [f"{start_date} 10:00"]  # Default fallback

#Main scheduling function
def schedule_advisor_function(candidate_message: str, current_date: str = None) -> Dict:
    current_date = current_date or datetime.now().strftime("%Y-%m-%d")

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""
You are a scheduling assistant helping a job interview coordinator.
Your task is to extract the candidate's preferred date (if any) and suggest available time slots.
Available slots: {slots}
Respond in JSON format:
{
  "preferred_date": "<date or empty>",
  "suggested_slots": [<list of slots>],
  "explanation": "<brief explanation>"
}
If no preferred date is mentioned, suggest slots starting from tomorrow.
"""),
        HumanMessage(content=f"""
Today's date is {current_date}.
Candidate message: "{candidate_message}"
""")
    ])

    # Use tomorrow as default preferred date
    default_date = (datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    #slots = mock_query_available_slots(default_date)
    slots = sql.check_dates(default_date)

    # Format and invoke the prompt
    messages = prompt.format_messages(slots=slots)
    response = llm.invoke(messages)

    # Basic parsing (ideally use a structured parser)
    content = response.content

    # Try to extract a date from the response
    for word in content.split():
        try:
            parsed = datetime.strptime(word, "%Y-%m-%d")
            preferred_date = parsed.strftime("%Y-%m-%d")
            suggested_slots = sql.check_dates(preferred_date, candidate_preferece=True)
            break
        except ValueError:
            preferred_date = default_date
            suggested_slots = slots
            continue

    # Fallback if no slots found
    if not suggested_slots:
        suggested_slots = fallback_slots(current_date)

    return {
        #"preferred_date": preferred_date,
        #"suggested_slots": suggested_slots,
        "explanation": content.strip()
    }

