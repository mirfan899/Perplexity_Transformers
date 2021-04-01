import requests

headers = {
    'Content-Type': 'application/json',
}

# you can use multiple languages supported by xlm-roberta-base model
data = '{"sentence":"this is a sentence"}'

response = requests.post('http://127.0.0.1:5000/api/perplexity_score', headers=headers, data=data)
print(response.text)
#curl -d '{"sentence":"this is a sentence"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/perplexity_score
