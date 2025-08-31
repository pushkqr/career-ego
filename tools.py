import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

class Tool:
    def __init__(self):
        self.pushover_user = os.getenv("PUSHOVER_USER")
        self.pushover_token = os.getenv("PUSHOVER_TOKEN")
        self.pushover_url = "https://api.pushover.net/1/messages.json"

        self.record_user_details_json = {
            "name": "record_user_details",
            "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email address of this user"
                    },
                    "name": {
                        "type": "string",
                        "description": "The user's name, if they provided it"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Any additional information about the conversation that's worth recording"
                    }
                },
                "required": ["email"],
                "additionalProperties": False
            }
        }

        self.record_unknown_question_json = {
            "name": "record_unknown_question",
            "description": "Always use this tool to record any question that couldn't be answered",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question that couldn't be answered"
                    },
                },
                "required": ["question"],
                "additionalProperties": False
            }
        }

        self.tools = [
            {"type": "function", "function": self.record_user_details_json},
            {"type": "function", "function": self.record_unknown_question_json},
        ]

    def push(self, message: str):
        """Send a push notification via Pushover"""
        print(f"Push: {message}")
        payload = {
            "user": self.pushover_user,
            "token": self.pushover_token,
            "message": message,
        }
        try:
            response = requests.post(self.pushover_url, data=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Push failed: {e}")

    def record_user_details(self, email, name="Name not provided", notes="not provided"):
        self.push(f"Recording interest from {name} with email {email} and notes {notes}")
        return {"recorded": "ok"}

    def record_unknown_question(self, question):
        self.push(f"Recording '{question}' asked that I couldn't answer")
        return {"recorded": "ok"}

    def handle_tool_calls(self, toolcalls):
        results = []
        for tool_call in toolcalls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"Tool called: {tool_name}", flush=True)
            tool = getattr(self, tool_name, None)

            if callable(tool):
                result = tool(**arguments)
            else:
                result = {"error": f"Tool '{tool_name}' not found"}

            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        return results
