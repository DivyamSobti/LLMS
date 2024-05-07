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
            {"role": "system", "content": "You are a personal Python tutor. Write and run code to answer Python questions.Only return the code no output, no explaining the code, no markdown."},
            {"role": "user", "content": "Write a Python code that generate a function call to this api: http://numbersapi.com/#random/math and assign the result to a variable called 'result'."},
            {"role": "user", "content": f"the number is {number}"},
        ]
    )
    url2=completion.choices[0].message.content
    code = url2.strip('` ')
    # Execute the code
    exec(code, globals())
    # result = get_math_fact(5)
    # # url2=url2.replace('number',number)
    # # Generate the API URL based on the user's input
    # url = f"http://numbersapi.com/{number}/math"

    # Fetch the fact from the Numbers API
    # response = requests.get(url)

    if 'result' in globals():
        # def generate_json_response():
        #     return jsonify({'fun_fact': result})
        jason = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a personal python tutor. Write and run code to answer python questions.Only return the code no output, no explaining the code, no markdown."},
                {"role": "user", "content": "write a pythin code which flask app can return a JSON response with a key 'fun_fact' and value as variable 'result',just need return statement"},
                {"role": "user", "content": "remove return from the return statement and it should have jsonify function from flask module"},
            ]
        )
        finalresult = jason.choices[0].message.content
        finalresult = finalresult.strip('`')
        exec(finalresult, globals())
        return result
        # return generate_json_response()

    else:
        return jsonify({'error': 'Could not retrieve the fact'}), 500

if __name__ == '__main__':
    app.run(debug=True) #logs will be displayed in the console
