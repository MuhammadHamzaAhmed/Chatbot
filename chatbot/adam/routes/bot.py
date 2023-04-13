from os import getcwd
from os.path import join, exists
from flask import request
from transformers import GPT2LMHeadModel, GPT2Tokenizer

import json
from adam import app, db
# from adam.training.trainer import ChatbotT5
from sqlalchemy import Column, Integer, Text
from fuzzywuzzy import fuzz

import traceback

class Bot(db.Model):
    __tablename__ = 'bot'

    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)


model_path = join(join(getcwd(), "adam"), "model")
dataset = join(join(join(getcwd(), "adam"), "dataset"), "preprocess.json")


@app.route("/")
def healthCheck():
    return "Working"

@app.route("/path")
def pathCheck5():
    return model_path

# chatbotT5 = ChatbotT5(model_path)
dataset = json.load(open(dataset, 'r'))

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data["question"]
        # try:
        #     chatbotT5.generate_response(question)
        # except:
        #     pass
        highest_similarity = 0
        most_similar_string = ''
        for obj in dataset:
            similarity = fuzz.token_set_ratio(question, obj['question'])
            if similarity > highest_similarity and similarity > 75:
                highest_similarity = similarity
                most_similar_string = obj['response']
        bot = Bot()
        bot.question = data["question"]
        bot.answer = most_similar_string
        db.session.add(bot)
        return {"response": most_similar_string}
    except Exception as e:
        traceback.print_exc()
        return {"response": str(e)}
