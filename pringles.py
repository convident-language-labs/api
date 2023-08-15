import openai
#import json
import os
openai.api_key = API_KEY = os.environ.get("OPENAI_KEY")

def pringles(replies, question):
    
    prompt= "Which of these replies is the best response for someone who said \""
    prompt = prompt + question + "\"?\n"
    
    for i in range(1, len(replies)+1):
        prompt = prompt + str(i) + ". " + replies[i-1] + "\n"
        
    prompt = prompt + "\nCompare based on relevance, clarity, tone, and style. Just answer with a single number, nothing else."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response["choices"][0]["message"]["content"]
    
if __name__ == "__main__":  
    replies = ['好的，现在就给你买冰淇淋吃。',
            '嗯，冰淇淋确实很好吃，我也想吃。',
            '哇，我也正好想吃冰淇淋呢！',
            '那我们一起去买冰淇淋吧，现在正好天气热。',
            '冰淇淋是个不错的选择，我也想吃一份。']
    question= '现在我要吃冰淇淋。'
    print(pringles(replies, question)) #currently returns 4.

    kr_replies = ['저도 사랑해요. ',
                '정말 감사해요.',
                '사랑하는 사람이 너라서 행복해요.',
                '항상 당신과 함께할 수 있어서 행복해요.',
                '사랑은 끝이 없어요.']
    kr_question = '사랑해요.'
    print(pringles(kr_replies, kr_question)) #currently returns 1

    cn2_replies = ['直接告诉她你对她有好感，然后邀请她出去。比如说：“我喜欢你，想一起出去吃个饭怎么样？”',
                '找出你们共同兴趣，然后提议一起去做这些事情。比如，如果你们都喜欢看电影，你可以邀请她一起去电影院。',
                '可以利用社交活动的机会邀请她出去。比如，如果有个派对或者演唱会，你可以问她是否想一起参加。',
                '提议一起吃个饭。这是一个很受欢迎的约会方式，可以给你们俩一个轻松的机会相互了解。',
                '如果你感到紧张，可以选择邀请她参加一个群体活动。比如，你可以组织一个小型聚会，邀请一些共同的朋友一起参加。']
    cn2_question = '现在我喜欢这个女生，可是我不知道约她出去怎么办。你可以帮我吗？'
    print(pringles(cn2_replies,cn2_question)) #currently returns 2