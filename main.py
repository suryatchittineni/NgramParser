import uvicorn
from fastapi import FastAPI, File, UploadFile
from n_gram_parser import NGramParser

app = FastAPI()

@app.post("/ngram", tags=["Ngram API"])
def get_frequency_for_n_number_of_consecutive_words(n: int, file: UploadFile = File(...)):
    service = NGramParser(n=n, file=file)
    return service.get_frequency_and_predictions()

@app.post("/frequency", tags=["Ngram API"])
def get_frequency_of_text(n: int, search_text: str, file: UploadFile = File(...)):
    service = NGramParser(n=n, file=file)
    return service.get_frequency_of_text(text=search_text)

@app.post("/predictions", tags=["Ngram API"])
def get_upto_x_number_of_predictions_after_a_given_text(n: int, x: int, search_text: str, file: UploadFile = File(...)):
    service = NGramParser(n=n, file=file)
    return service.get_predictions(x=x, text=search_text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)