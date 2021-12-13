# NgramParser
Parse a file and return word frequencies, predict the patterns.

* Setup
    1. Create virtual env
        
            python3 -m venv .venv

    2. Load virtual env
        
            source .venv/bin/activate

    3. Install fastapi
    
            pip install fastapi

    4. Install uvicorn
    
            pip install "uvicorn[standard]"

    5. Install pytest
    
            pip install -U pytest
        
    6. Install magic mock
        
            pip install pytest-mock

* Run
    1. Run the app
        
            uvicorn main:app --reload

    3. Run tests
        
            pytest

            pytest -vv
