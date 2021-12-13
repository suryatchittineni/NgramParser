# NgramParser
Parse a file and return word frequencies, predict the patterns.

* Setup
    1. Create virtual env
        
            python3 -m venv .venv

    2. Load virtual env
        
            source .venv/bin/activate

    3. Install dependencies
    
            pip install -r requirements.txt

* Run
    1. Run the app
        
            uvicorn main:app --reload

    3. Run tests
        
            pytest -vv
