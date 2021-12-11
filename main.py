import uvicorn
from fastapi import FastAPI, File, UploadFile
from n_gram_parser import NGramParser

app = FastAPI()

@app.post("/frequency")
def frequency_of_n_consecutive_words(n: int, file: UploadFile = File(...)):
    service = NGramParser(n=n, file=file)
    return service.run()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)