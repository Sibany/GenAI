from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate
from langchain.tools import Tool

# Import your advisor functions
from module_2 import info_advisor_fun_ction
from module_schedule import schedule_advisor_function
from module_exit import exit_advisor_function

# Define tools
exit_advisor_tool = Tool.from_function(
    name="exit_advisor",
    func=exit_advisor_function,
    description="Decides if the conversation should end based on candidate's intent."
)

schedule_advisor_tool = Tool.from_function(
    name="schedule_advisor",
    func=schedule_advisor_function,
    description="Checks recruiter calendar and validates interview time slots."
)

info_advisor_tool = Tool.from_function(
    name="info_advisor",
    func=info_advisor_fun_ction,
    description="Engages the candidate through conversation, asking relevant questions to assess their suitability for the position and determine whether it's time to proceed to scheduling."
)

# Define prompt
main_agent_prompt = ChatPromptTemplate.from_messages([
    
("system", """
You are the MAIN AGENT responsible for managing a conversation with a job candidate.

You will receive the full conversation history as input. Use this to determine the next best action, incorporating input from your advisor tools.
You must give your advisors the full conversation history as input in order for them to give a well-founded recomendation

Follow this process:
1. Call 'exit_advisor' to check if the conversation should end. If 'should_end' is True, politely close the conversation and do not proceed to other advisors.
2. Call 'info_advisor' to assess whether the candidate meets at least two job requirements. 
     - If 'schedule': is no,  do not proceed to the next advisor.
       The two job requirements bar has not been met. the advisor will specify all the required qualifications under 'required qualifications'.
       Ask targeted questions to explore additional qualifications and respond to any candidate inquiries.
     - If 'schedule': is yes, proceed to the next advisor.

3. Call 'schedule_advisor' and aim to guide the conversation toward scheduling an interview, offer options from the slots provided by the advisor. 

**Keep your responses short an focused under 30 tokens.**
Always aim to guide the conversation toward scheduling an interview. If the candidate agrees, suggest a time slot from 'schedule_advisor'.
"""),
    ("human", "{input}"),
    ("ai", "{agent_scratchpad}")
])


# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

# Create agent
agent = create_openai_tools_agent(
    llm=llm,
    tools=[exit_advisor_tool, schedule_advisor_tool, info_advisor_tool],
    prompt=main_agent_prompt
)

# Wrap in executor
main_agent = AgentExecutor(
    agent=agent,
    tools=[exit_advisor_tool, schedule_advisor_tool, info_advisor_tool],
    verbose=True,
    return_intermediate_steps=True    # ✅ Only return final output
)
