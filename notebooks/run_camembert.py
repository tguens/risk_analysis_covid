import json
import transformers
from transformers import AutoTokenizer, AutoModelWithLMHead


if __name__ == "__main__":
    #run_scrap()
    #ms = json.load9)
    path = "../data/Macky_Sall_twitter.json"
    with open(path, 'r') as reader:
        tweets = json.load(reader)
    print('debug')
    #First step in building a model
    tokenizer = AutoTokenizer.from_pretrained("camembert-base")
    model = AutoModelWithLMHead.from_pretrained("camembert-base")
    
