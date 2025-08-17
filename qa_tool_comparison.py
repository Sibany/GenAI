import json
from app_main_new import main_agent

# Load transformed conversation data
with open("transformed_sms_conversations.json", "r", encoding="utf-8") as f:
    transformed_data = json.load(f)

# Prepare output list
qa_results = []

# Iterate through each entry and invoke the agent
for entry in transformed_data:
    conversation_id = entry["conversation_id"]
    turn_id = entry["turn_id"]
    input_text = entry["text"]
    original_tool = entry["last_tool_used"]

    # Send to main_agent and extract last tool used
    agent_response = main_agent.invoke({"input": input_text})
    intermediate_steps = agent_response.get("intermediate_steps", [])

    if intermediate_steps:
        last_tool_name = intermediate_steps[-1][0].tool  # e.g., "info_advisor"
        test_tool = last_tool_name.split("_")[0].capitalize()  # → "Info"
    else:
        test_tool = "None"

    # Append result
    qa_results.append({
        "conversation_id": conversation_id,
        "turn_id": turn_id,
        "test_result_last_tool_used": test_tool,
        "sms_conversations_last_tool_used": original_tool
    })

# Save results to a new JSON file
with open("qa_tool_comparison_results.json", "w", encoding="utf-8") as f:
    json.dump(qa_results, f, indent=2)

print("✅ QA tool comparison complete. Results saved to 'qa_tool_comparison_results.json'.")
