#Definimos acá función para poder importarla desde otros modulos

import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

def get_embedding(text: str) -> np.ndarray:
    load_dotenv('./openAI.env')
    client = OpenAI(api_key=os.environ.get('openai_apikey'))
    resp = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return np.array(resp.data[0].embedding, dtype=np.float32)

def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
