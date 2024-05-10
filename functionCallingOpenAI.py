import os
import requests
from openai import OpenAI
import json

client = OpenAI()
def get_math_fact(number):
    """Fetches a math fact about a number from the Numbers API"""
    base_url = "http://numbersapi.com/"
    url = f"{base_url}{number}/math"
    response = requests.get(url)
    result = {
        "fun_fact": response.text
    }
    return json.dumps(result)

def run_conversation(content):
    messages = [{"role": "user", "content": content}]
    functions = [{
        "name": "fetch_fun_fact",
        "description": "Fetches a fun fact about a given number from the Numbers API",
        "parameters": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "number",
                    "description": "The number to fetch the fact about e.g. 42"
                }
            },
            "required": ["number"]
        }
    }]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    response_message = response.choices[0].message
    function_call = response_message.function_call

    if function_call:
        messages.append(response_message)
        available_functions = {
            "fetch_fun_fact": get_math_fact,
        }
        function_name = function_call.name
        function_to_call = available_functions[function_name]
        function_args = json.loads(function_call.arguments)
        function_response = function_to_call(number=function_args.get("number"))
        print(f"API response: {function_response}")
        messages.append({
            "role": "function",
            "name": function_name,
            "content": function_response
        })

        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto"
        )
        return second_response

if __name__ == "__main__":
    question = input("Enter a number to get a math fact: ")
    response = run_conversation(question)
    for chunk in response.choices:
        print(chunk.message.content or "", end='', flush=True)
