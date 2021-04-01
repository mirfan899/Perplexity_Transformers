## Install
Run the following commands in terminal to install the requirements for project.
```shell
pip install -r requirements.txt
```
It will take some time because it is using the PyTorch and Transformers models.

## Run the server
For the first time when you run the flask server it will download the models(XLM-ROBERTA-BASE) for
perplexity. After that model will be available for use whenever you run the server.

## Testing
For testing, you can run the script `test_api.py` with your own sentences to get the perplexity score.
You can also use the `curl` command to test the api
```shell
curl -d '{"sentence":"this is a sentence"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/perplexity_score
```

For getting the time of execution of API request, use time
```shell
time curl -d '{"sentence":"this is a sentence"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/api/perplexity_score
```