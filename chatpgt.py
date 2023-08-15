import openai
import os
openai.api_key = API_KEY = os.environ.get("OPENAI_KEY")
  

def gptcall(situation, vocab, micro_situational_vocab):
    message_list = []
    message_list.append(
        {'role': 'system', 'content': situation + "\n Response will be made up of words in this list:" + vocab + "\n Potential phrases used will consist of words in this list: " + micro_situational_vocab }
    )

def call(content):
    message_list=[]
    message = [{"role": "user", "content": "You are in a conversation with someone. They just said " + content + ". Generate a response to what they said."}]
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        n=5
    )
    
    for choice in completion.choices:
        message_list.append(choice.message.content)
        print(choice.message.content)
    return message_list

if __name__ == "__main__":  
    message_list = []
    while True:
        content = input("User: ") #replace with stt
        message_list.append({"role": "user", "content": content})
        

        
        for i in range(5):
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_list
            )
            chat_response = completion.choices[0].message.content
            #instead of print call Nick's method for choosing best response
            print(f'John: {chat_response}')
        message_list.append({'role': 'assistant', 'content': chat_response})
    
