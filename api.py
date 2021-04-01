from flask import Flask
from flask_restful import Resource, Api, reqparse
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
model = AutoModelForMaskedLM.from_pretrained("xlm-roberta-base").to("cuda")


def get_score(sentence):
    encodings = tokenizer(sentence, return_tensors='pt')
    print(encodings.input_ids.size(1))
    max_length = 1024
    stride = 512

    lls = []

    for i in range(0, encodings.input_ids.size(1), stride):
        begin_loc = max(i + stride - max_length, 0)
        end_loc = min(i + stride, encodings.input_ids.size(1))
        trg_len = end_loc - i  # may be different from stride on last loop
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to("cuda")
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            log_likelihood = outputs[0] * trg_len

        lls.append(log_likelihood)

    ppl = torch.exp(torch.stack(lls).sum() / end_loc)

    print(ppl.item())
    return {"sentence": sentence, "score": ppl.item()}


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("sentence", required=True, type=str, help="please provide the sentence to get perplexity score.")


class Perplexity(Resource):
    def get(self):
        return {"message": "Welcome to Transformers Perplexity API", "status": 200}

    def post(self):
        args = parser.parse_args()
        if args["sentence"]:
            print(args["sentence"])
            result = get_score(args["sentence"])
            return result
        else:
            return {"You should provide a sentence."}


api.add_resource(Perplexity, '/api/perplexity_score')

if __name__ == '__main__':
    app.run(debug=False, threaded=False, processes=1)
