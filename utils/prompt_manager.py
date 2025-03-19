def format_messages(system_prompt, conversation_history, candidate_info, current_state):
    formatted_messages = [{"role": "system", "content": system_prompt}]
    
    info_prompt = "Current candidate information:\n"
    
    for key, value in candidate_info.items():
        if key == "conversation_completed" or key == "questions_asked":
            continue
            
        if value:
            if key == "tech_stack" and isinstance(value, list):
                info_prompt += f"- {key}: {', '.join(value)}\n"
            else:
                info_prompt += f"- {key}: {value}\n"
        else:
            info_prompt += f"- {key}: Not provided yet\n"
    
    if current_state == "gathering_info":
        info_prompt += "\nGuidance: The candidate has not provided all required information. Ask for missing information in a conversational manner."
    elif current_state == "ask_technical_questions":
        info_prompt += "\nGuidance: All basic information has been collected. Ask technical questions based on the candidate's tech stack."
    elif current_state == "conversation_complete":
        info_prompt += "\nGuidance: All information has been collected and technical questions have been asked. Thank the candidate and conclude the conversation."
    
    formatted_messages.append({
        "role": "system",
        "content": info_prompt
    })
    
    chat_history = conversation_history.copy()
    for message in chat_history:
        formatted_messages.append({
            "role": message["role"],
            "content": message["content"]
        })
    
    return formatted_messages