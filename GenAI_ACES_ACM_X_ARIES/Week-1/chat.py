import json
import google.generativeai as genai
import requests

grok_history = []
gemini_history = []


def grok(prompt, role, grok_history):
    api_key = "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"
    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "meta-llama/llama-4-scout-17b-16e-instruct"

    grok_history.append({"role": role, "content": prompt})
    payload = {
        "model": model,
        "messages": grok_history,
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + api_key}
    payload = json.dumps(payload)
    response = (requests.request("POST", url, headers=headers, data=payload)).json()
    # print(response)
    grok_history.append({"content": response["choices"][-1]['message']['content'], "role": 'assistant'})
    return grok_history[-1]["content"]


def gemini(prompt, gemini_history):
    genai.configure(api_key="AIzaSyAr41v6FWXjCT21O34cce-QZG1SPiLeEO8")
    gemini_history.append({
        'role': "user",
        'parts': [{'text': prompt}]
    })
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(gemini_history)
    gemini_history.append({
        'role': 'model',
        'parts': [{'text': response.text}]
    })
    return response.text


def agent_conversation(user_question, max_rounds=3):
    """
    Let Agent A (Groq) and Agent B (Gemini) converse with each other
    Agent A: Domain Expert
    Agent B: Critic/Validator
    Discussion happens silently, only final answer is shown
    """

    conversation_grok = []
    conversation_gemini = []

    # Agent A (Groq) - Initial expert response
    expert_prompt = f"""You are a domain expert. Answer this question directly and professionally: "{user_question}"

    Provide a clear, accurate, and comprehensive response. Focus only on answering the question without mentioning any validation or feedback process."""

    agent_a_response = grok(expert_prompt, "user", conversation_grok)
    current_response = agent_a_response

    # Multi-round conversation between agents (silent)
    for round_num in range(max_rounds):
        # Agent B (Gemini) - Critic/Validator
        critic_prompt = f"""Review this response for accuracy and completeness and if it is simple greeting then don't validate and reply politely:

        Question: "{user_question}"
        Response: "{current_response}"

        If the response is accurate and complete, respond with "APPROVED".
        If not, provide specific issues that need to be fixed, but keep your feedback concise and technical."""

        agent_b_feedback = gemini(critic_prompt, conversation_gemini)

        # Check if Agent B approved the response
        if "APPROVED" in agent_b_feedback.upper():
            break

        # Agent A (Groq) - Refine based on feedback
        if round_num < max_rounds - 1:
            refine_prompt = f"""Based on feedback about your previous response, please provide an improved answer to: "{user_question}"

            Focus on accuracy, completeness, and clarity. Give a direct, professional response without mentioning the feedback process or validation."""

            refined_response = grok(refine_prompt, "user", conversation_grok)
            current_response = refined_response

    return current_response, agent_b_feedback


# Main conversation loop with silent agent discussion
print("🚀 Multi-Agent AI Chat System")
print("Agent A (Groq): Domain Expert | Agent B (Gemini): Critic/Validator")
print("Agents discuss silently in background - you see only final validated answers")
print("Type 'exit' to quit")
print("-" * 60)

# Initial system setup
prompt = "You are Agent A, a domain expert. Ask the user how you can help them in one line only."
role = "system"
initial_greeting = grok(prompt, role, grok_history)
print(f"🤖 Agent A: {initial_greeting}")
role = "user"

while True:
    user_input = input("\nYou> ").strip()

    if user_input.lower() == "exit":
        break

    if not user_input:
        print("Please enter a valid question.")
        continue

    try:
        # Agents discuss the question silently
        final_response, final_validation = agent_conversation(user_input)


        print(f"\n{final_response}")

        # Add to main conversation history for context
        grok_history.append({"role": "user", "content": user_input})
        grok_history.append({"role": "assistant", "content": final_response})

    except Exception as e:
        print(f"❌ Error during agent conversation: {str(e)}")
        print("Please try again or type 'exit' to quit.")

print("👋 Bye!")