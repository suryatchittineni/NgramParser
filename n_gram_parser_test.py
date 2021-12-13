import io
import pytest
from os import read
from fastapi import UploadFile, HTTPException
from n_gram_parser import NGramParser
from mock_output_test1 import output1_test1, output2_test1


input1 = open("input1.txt", "rb")
input1_file_content = input1.read()

input2 = open("input2.txt", "rb")
input2_file_content = input2.read()

'''
    Structure of the parameters
    Parameter: tuple
    input: list with first element n
    expected: expected result
'''
@pytest.mark.parametrize(
    "input, expected", 
    [
        (
            5, 
            output1_test1
        ),
        (
            2,
            output2_test1
        )
    ]
)
def test_get_frequency_and_predictions(input, expected):
    file_content = None
    if input == 5:  
        file_content = io.BytesIO(input2_file_content)
    if input == 2:
        file_content = io.BytesIO(input1_file_content)
    file = UploadFile(...)
    file.file = file_content
    service = NGramParser(n=input, file=file)
    output = service.get_frequency_and_predictions()
    assert output == expected


'''
    Structure of the parameters
    Parameter: tuple
    input: list with first element n, second element search_text
    expected: expected result
'''
@pytest.mark.parametrize(
    "input, expected", 
    [
        (
            [3, "we're"], 
            {
                "Frequency of [we're]": 3
            }
        ),
        (
            [3, "fly"],
            {
                "Frequency of [fly]": 3
            }
        ),
        (
            [3, "fly fly"],
            {
                "Frequency of [fly fly]": 2
            }
        ),
        (
            [5, "project"],
            {
                "Frequency of [project]": 3
            }
        ),
        (
            [5, "ALICE'S"],
            {
                "Frequency of [alice's]": 5
            }
        )
    ]
)
def test_get_frequency_of_text(input, expected):
    file_content = None
    if input == [3, "we're"] or input == [3, "fly"] or input == [3, "fly fly"]:  
        file_content = io.BytesIO(input2_file_content)
    if input == [5, "project"] or input == [5, "ALICE'S"]:
        file_content = io.BytesIO(input1_file_content)
    file = UploadFile(...)
    file.file = file_content
    service = NGramParser(n=input[0], file=file)
    output = service.get_frequency_of_text(text=input[1])
    assert output == expected


'''
    Structure of the parameters
    Parameter: tuple
    input: list with first element n, second element x, thirt element search_text
    expected: expected result
'''
@pytest.mark.parametrize(
    "input, expected", 
    [
        (
            [3, 3, "we're"], 
            {
                "candidate completions for [we're]": {
                    "going": 2,
                    "birds": 1
                }
            }
        ),
        (
            [3, 2, "fly"],
            {
                "candidate completions for [fly]": {
                    "fly": 2,
                    "away": 1
                }
            }
        ),
        (
            [3, 2, "fly fly"],
            {
                "candidate completions for [fly fly]": {
                    "away": 1,
                    "fly": 1
                }
            }
        ),
        (
            [5, 5, "project"],
            {
                "candidate completions for [project]": {
                    "gutenberg": 3
                }
            }
        ),
        (
            [5, 5, "alice's"],
            {
                "candidate completions for [alice's]": {
                    "adventures": 4,
                    "evidence": 1
                }
            }
        )
    ]
)
def test_get_predictions(input, expected):
    file_content = None
    if input == [3, 3, "we're"] or input == [3, 2, "fly"] or input == [3, 2, "fly fly"]:  
        file_content = io.BytesIO(input2_file_content)
    if input == [5, 5, "project"] or input == [5, 5, "alice's"]:
        file_content = io.BytesIO(input1_file_content)
    file = UploadFile(...)
    file.file = file_content
    service = NGramParser(n=input[0], file=file)
    output = service.get_predictions(x=input[1], text=input[2])
    assert output == expected


def test_get_predictions_has_exception(mocker):
    input = [3, 3, "we're"]
    mocker.patch.object(NGramParser, 'parse_data', side_effect=Exception)
    file_content = None
    if input == [3, 3, "we're"]:  
        file_content = io.BytesIO(input2_file_content)
    file = UploadFile(...)
    file.file = file_content
    service = NGramParser(n=input[0], file=file)
    try:
        service.get_predictions(x=input[1], text=input[2])
        assert False
    except HTTPException as e:
        print(e.detail)
        assert e.detail["msg"] == "Something went wrong while getting predictions of text."
        assert e.status_code == 500


def test_get_frequency_of_text_has_exception(mocker):
    input = [3, "fly"]
    mocker.patch.object(NGramParser, 'parse_data', side_effect=Exception)
    file_content = None
    if input == [3, "fly"]:  
        file_content = io.BytesIO(input2_file_content)
    file = UploadFile(...)
    file.file = file_content
    service = NGramParser(n=input[0], file=file)
    try:
        service.get_frequency_of_text(text=input[1])
        assert False
    except HTTPException as e:
        print(e.detail)
        assert e.detail["msg"] == "Something went wrong while getting frequency of text."
        assert e.status_code == 500


def test_get_frequency_of_text_has_exception(mocker):
    input = 3
    mocker.patch.object(NGramParser, 'parse_data', side_effect=Exception)
    file_content = None
    if input == 3:  
        file_content = io.BytesIO(input2_file_content)
    file = UploadFile(...)
    file.file = file_content
    service = NGramParser(n=input, file=file)
    try:
        service.get_frequency_and_predictions()
        assert False
    except HTTPException as e:
        print(e.detail)
        assert e.detail["msg"] == "Something went wrong while getting frequencies and predictions."
        assert e.status_code == 500