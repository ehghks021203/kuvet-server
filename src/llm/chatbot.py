import os
import sys
from datetime import datetime
import pytz
import openai
import chromadb
from chromadb.utils import embedding_functions
sys.path.append(os.path.dirname(os.path.abspath('')))
from config import chatbot, api

# ChatGPT Setting
openai.api_key = api.OPENAI_API_KEY
MODEL = chatbot.MODEL

def chat(msg: str, history: list = []):
    messages = []
    SYSTEM_MSG = chatbot.SYSTEM_PROMPT

    messages.append({"role":"system", "content":SYSTEM_MSG})
    history.append({"role":"user", "content":msg})
    messages.extend(history)

    chatbot = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )

    bot_msg = chatbot["choices"][0]["message"]["content"]
    history.append({"role":"assistant", "content":bot_msg})
    
    return bot_msg, history

def text_embedding(text):
    response = openai.Embedding.create(model="text-embedding-ada-002", input=text)
    return response["data"][0]["embedding"]

def rag(msg: str, history: list = []):
    messages = []
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                model_name="text-embedding-ada-002"
            )

    client = chromadb.PersistentClient(path=chatbot.CHROMA_DB_PATH)
    disease_collection = client.get_collection("disease",embedding_function=openai_ef)
    medicine_collection = client.get_collection("medicine",embedding_function=openai_ef)

    # 사용자 입력
    vector = text_embedding(msg)

    results = disease_collection.query(    
        query_embeddings = vector,
        n_results = 3,
        include = ["documents"]
    )

    disease_res = "\n".join(str(item) for item in results["documents"][0])
    
    results = medicine_collection.query(    
        query_embeddings = vector,
        n_results = 5,
        include = ["documents"]
    )

    medicine_res = "\n".join(str(item) for item in results["documents"][0])

    sys_prompt = f'''
    {chatbot.SYSTEM_PROMPT}
    You are a helpful assistant and you must answer in 50 characters or less. 
    Your answer should be output in a conversational format and should be concise. 
    You should describe the disease name, symptoms, diagnosis, prevention, and treatment. 
    If the question is not about the animal's symptoms or the animal's medicine, help the user rephrase the question to ask about symptoms.

    질병 관련 Context:
    {disease_res}
    
    You must describe the drug's product name, effects, dosage, and warnings
    의약품 관련 Context:
    {medicine_res}
    '''
    with open("./prompt.txt", "w") as f:
        f.write(sys_prompt)

    messages.append({"role":"system", "content":sys_prompt})
    history.append({"role":"user", "content":msg, "timestamp": datetime.now(pytz.timezone('Asia/Seoul')).strftime('%p %I:%M').replace('AM', '오전').replace('PM', '오후')})
    messages.extend(history)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1
    )
    bot_msg = response["choices"][0]["message"]["content"]
    bot_timestamp = datetime.now(pytz.timezone('Asia/Seoul')).strftime('%p %I:%M').replace('AM', '오전').replace('PM', '오후')
    history.append({"role":"assistant", "content":bot_msg, "timestamp": bot_timestamp})

    return bot_msg, bot_timestamp, history

if __name__ == "__main__":
    first = True
    history = []
    while True:
        if first:
            print("Bot >> ", end="")
            msg, history = rag("안녕", history)
            print(msg)
            first = False
        print("Message >> ", end="")
        input_str = input();
        print("Bot >> ", end="")
        msg, history = rag(input_str, history)
        print(msg)