from flask import Flask, request, jsonify
from openai import OpenAI
import requests

app = Flask(__name__)

client = OpenAI()

@app.route('/fun-fact', methods=['GET'])
def fun_fact():
    # Get the number from the user's query parameter
    number = request.args.get('number', 'random')
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a personal python tutor. Write and run code to answer python questions.Only return the code no output, no explaining the code, no markdown."},
                {"role": "user", "content": "Write a Python code block that generate a function call to this api: http://numbersapi.com/#random/math and assign the result to a variable called 'result'. After getting the result it checks the i want to store the result in variable 'output'. the 'output' should be a json object with key 'fun_fact' and value reult of the variable 'result'."},
                # {"role": "user", "content": "remove return from the return statement and it should have jsonfy function from flask module"},
                {"role": "user", "content": f"the number is {number}"},
                {"role": "user", "content": "the 'output' should be flask jsonify object"},
            ]
    )
    finalOutput=completion.choices[0].message.content
    code = finalOutput.strip('` ')
    # Execute the code
    exec(code, globals())

    if 'output' in globals():
        return output
    else:
        return jsonify({'error': 'Could not retrieve the fact'}), 500

if __name__ == '__main__':
    app.run(debug=True) #logs will be displayed in the console
