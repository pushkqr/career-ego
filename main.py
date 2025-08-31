import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from pydantic import BaseModel
from prompts import Prompt
from tools import Tool

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
model_name = "gemini-2.5-flash"
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

class Evaluation(BaseModel):
    is_acceptable: bool
    feedback: str


class App:
    def __init__(self):
        self.gemini = OpenAI(api_key=api_key, base_url=base_url)
        self.tool = Tool()
        self.prompt = Prompt()

    def evaluate(self, reply, message, history) -> Evaluation:
        message = [
            {"role": "system", "content": self.prompt.evaluator_system_prompt},
            {"role": "user", "content": self.prompt.evaluator_user_prompt(reply, message, history)}
        ]
        response = self.gemini.beta.chat.completions.parse(model=model_name, messages=message, response_format=Evaluation)
        return response.choices[0].message.parsed

    def rerun(self, reply, message, history, feedback):
        updated_system_prompt = self.prompt.system_prompt + "\n\n## Previous answer rejected\nYou just tried to reply, but the quality control rejected your reply\n"
        updated_system_prompt += f"## Your attempted answer:\n{reply}\n\n"
        updated_system_prompt += f"## Reason for rejection:\n{feedback}\n\n"
        messages = [{"role": "system", "content": updated_system_prompt}] + history + [{"role": "user", "content": message}]
        response = self.gemini.chat.completions.create(model=model_name, messages=messages)
        return response.choices[0].message.content

    def chat(self, message, history):      
        messages = [{"role": "system", "content": self.prompt.system_prompt}] + history + [{"role": "user", "content": message}] 
        reply = ""
        response = self.gemini.chat.completions.create(model=model_name, messages=messages, tools=self.tool.tools)

        if response.choices[0].finish_reason == "tool_calls":
            tool_results = self.tool.handle_tool_calls(response.choices[0].message.tool_calls)
            messages.append(response.choices[0].message)
            messages.append(tool_results)
            response = self.gemini.chat.completions.create(model=model_name, messages=messages)
            
        reply = response.choices[0].message.content

        evaluation = self.evaluate(reply,message,history)
        if not evaluation.is_acceptable:
            reply = self.rerun(reply, message, history, evaluation.feedback)       
            
        return reply

if __name__ == "__main__":
    app = App()
    gr.ChatInterface(app.chat, type="messages").launch()