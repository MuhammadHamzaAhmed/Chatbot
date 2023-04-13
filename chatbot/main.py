from adam import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# import json
# import torch
# import pandas
# from torch.utils.data import Dataset, DataLoader
# from transformers import DistilBertTokenizerFast, DistilBertForQuestionAnswering, Trainer, TrainingArguments
# from datasets import Dataset
# import pandas as  pd

# data = json.load(open('./adam/dataset/preprocess.json', 'r'))





# bot = ChatbotT5("model")
# # data = bot.prepare_data(data)
# # bot.fine_tune(data, data)
# print(bot.generate_response("How are top 10 subnet by IP address are displayed on dashboard?"))