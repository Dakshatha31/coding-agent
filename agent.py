
import json
import os
from openai import OpenAI
from config import MODEL, MAX_STEPS
from prompts import SYSTEM_PROMPT
from tools.registry import TOOL_SPECS, execute_tool

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def run_agent(task, prior_messages=None):
    activity = []
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if prior_messages:
        for m in prior_messages[-8:]:
            if m.get("role") in ("user", "assistant") and m.get("content"):
                messages.append({
                    "role": m["role"],
                    "content": m["content"]
                })

    messages.append({"role": "user", "content": task})

    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SPECS,
            tool_choice="auto",
            temperature=0.2
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or "No text response returned.", activity

        messages.append(message)

        for call in message.tool_calls:
            name = call.function.name

            try:
                args = json.loads(call.function.arguments or "{}")
                result = execute_tool(name, args)
            except Exception as exc:
                result = {"error": str(exc)}

            activity.append(f"Step {step + 1}: {name}")
            activity.append(str(result))

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result)
            })

    return "Maximum agent steps reached.", activity
