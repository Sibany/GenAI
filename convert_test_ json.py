import json

# Define label mapping
label_mapping = {
    "schedule": "Schedule",
    "end": "Exit",
    "continue": "Info"
}

# Load the JSON data from the file
with open("sms_conversations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare the transformed data
transformed_data = []

# Iterate through each conversation
for conversation in data:
    conversation_id = conversation["conversation_id"]
    turns = conversation["turns"]
    history = []

    for turn in turns:
        turn_id = turn["turn_id"]
        text = turn["text"]
        label = turn["label"]

        # Only include odd turns excluding turn_id 1
        if turn_id % 2 == 1 and turn_id != 1 and label in label_mapping:
            transformed_data.append({
                "conversation_id": conversation_id,
                "turn_id": turn_id,
                "text": " ".join(history),
                "last_tool_used": label_mapping[label]
            })

        # Append current turn text to history for future turns
        history.append(text)

# Save the transformed data to a new JSON file
with open("transformed_sms_conversations.json", "w", encoding="utf-8") as f:
    json.dump(transformed_data, f, indent=2)

print("Transformation complete. Output saved to 'transformed_sms_conversations.json'.")
