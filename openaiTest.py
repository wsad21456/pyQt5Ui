# coding=utf-8
import openai
import json
import os

openai.api_key = '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'

def dell(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message)
    return str(completion.choices[0].message)

if __name__ == '__main__':
    r = dell('GPT-3.5 turbo模型和GPT-3模型有什么区别？')
    response = json.loads((r))
    print(response['content'])