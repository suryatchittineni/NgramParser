from collections import defaultdict
import re
from fastapi.params import File
from fastapi import status, HTTPException


class NGramParser:
    n: int
    file: File
    frequency_map: defaultdict(list)
    prediction_map: defaultdict(list)
    words: list

    def __init__(self, n: int, file: File):
        self.n = n
        self.file = file
        self.frequency_map = defaultdict(lambda: 0)
        self.words = []
        self.prediction_map = defaultdict(list)

    """
    This method returns the frequency and prediction maps for the entire file
    """

    def get_frequency_and_predictions(self) -> dict:
        try:
            self.run()
            return {"Frequencies": self.frequency_map, "Predictions": self.prediction_map}
        except Exception as e:
            print(e) # In a real world scenario we will be logging here so that we can track these errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= {
                    "msg": "Something went wrong while getting frequencies and predictions.",
                    "additional details": e.args
                }
            )

    """
    This method will returns the number of occurances of a given text.
    """

    def get_frequency_of_text(self, text: str) -> dict:
        try:
            self.run()
            result = {f"Frequency of [{text.lower()}]": 0}
            if text.lower() in self.frequency_map:
                result[f"Frequency of [{text.lower()}]"] = self.frequency_map[text.lower()]
            return result
        except Exception as e:
            print(e) # In a real world scenario we will be logging here so that we can track these errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= {
                    "msg": "Something went wrong while getting frequency of text.",
                    "additional details": e.args
                }
            )
        
    """
    This method will get x number of predictions based on highest number of occurances.
    1. If all the words have same occurances we will just choose top x items from the list.
    2. Prediction are based on n number of words list created.
    """

    def get_predictions(self, x: int, text: str) -> dict:
        try:
            self.run()
            result = {f"candidate completions for [{text.lower()}]": {}}
            if text.lower() in self.prediction_map:
                next_words_set = set(self.prediction_map[text.lower()])
                next_words = self.prediction_map[text.lower()]
                predictions = {}
                for item in next_words_set:
                    predictions[item] = next_words.count(item)
                predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
                predictions = predictions[:x] if x < len(predictions) else predictions
                result[f"candidate completions for [{text.lower()}]"] = dict(predictions)
            return result
        except Exception as e:
            print(e) # In a real world scenario we will be logging here so that we can track these errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= {
                    "msg": "Something went wrong while getting predictions of text.",
                    "additional details": e.args
                }
            )

    """
    This method is just orchestrating the flow of data.
    """

    def run(self):
        self.parse_data()
        self.frequency_collector()

    """
    This method is parsing the file and creating a list with all the words in the file.
    We are using regex to use multiple delimiters to split the text.
    """

    def parse_data(self):
        file_content = self.file.file.readlines()
        for line in file_content:
            content = line.decode("utf-8")
            content = content.replace("\r\n", "")
            self.words.extend(
                re.split(r"[ \.,!\[\]:#*”“(){}?\-_\+<>^$%@~;\|]", content)
            )
        while "" in self.words:
            self.words.remove("")

    """
    This method is iterating through the words list generated from the file and creating map for the following:
    Frequency of word sequence based on provided n (number of words)
    Predictions of next word that occurs after a given sequence
    """

    def frequency_collector(self):
        start_index = 0
        end_index = self.n
        while len(self.words) >= self.n:
            current_words = []
            for i in range(start_index, end_index):
                current_words.append(self.words[i].lower())
                current_string = " ".join(current_words)
                if i != len(self.words) - 1:
                    self.prediction_map[current_string].append(
                        self.words[i + 1].lower()
                    )
                self.frequency_map[current_string] += 1
            self.words.pop(0)
