import re
from fastapi.params import File


class NGramParser:
    n: int
    file: File
    out_put: dict
    words: list

    def __init__(self, n: int, file: File):
        self.n = n
        self.file = file
        self.out_put = {}
        self.words = []

    def run(self) -> dict:
        self.parse_data()
        self.frequency_collector()
        return self.out_put

    def parse_data(self):
        file_content = self.file.file.readlines()
        for line in file_content:
            # \.\+,:;-_\"$\|
            content = line.decode("utf-8")
            content = content.replace("\r\n", "")
            self.words.extend(re.split(r"[ \.,]", content))
        while "" in self.words:
            self.words.remove("")
    
    def frequency_collector(self):
        start_index = 0
        end_index = self.n
        while len(self.words) >= self.n:
            current_words = []
            for i in range(start_index, end_index):
                current_words.append(self.words[i].lower())
                current_string = " ".join(current_words)
                if current_string in self.out_put:
                    self.out_put[current_string] += 1
                else:
                    self.out_put[current_string] = 1
            self.words.pop(0)

