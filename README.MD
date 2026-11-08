# Title: Is It a Plane or a Bird?

## Authors: 
- Shriya Shah
- Dana Chen
- Chloe Chen
- Vincy Cai

## Description:
This program analyzes an image of a flying object and tells you if its a bird, plane, or neither! 

## Process:
- Take image
- Use gemini to make sure not random thing, either bird or plane
- Scan for plane data
- If planes nearby, ask gemini to see which plane, then print plane information
- If no planes/image doesnt match, send to bird classifier
- Bird classifier checks, prints bird info + facts from gemini

## Setting up .env:
.env.example --- copy this into .env using:
- cp .env.example .env
- In .env, replace enter_id and enter_key with your your own keys:
    - OPENSKY_CLIENT_ID & OPENSKY_CLIENT_SECRET: https://opensky-network.org/my-opensky/account 
        - Create an account by following the link and generate your id and secret
    - GEMINI_API_KEY: https://aistudio.google.com/api-keys
        - Sign in if not already
        - Click "Create API key" in top right corner of page
        - Follow steps to create an API key
        - Copy the API key and paste it in .env where it says "enter_key" (replace it)

## Steps to run program:

### For Windows:
- In root folder run:
    - python -m venv venv
    - source venv/Scripts/activate
    - pip install -r requirements.txt
        - If there is a notice saying to update pip, copy the command and paste it in terminal to update pip.
    - pip install pillow
    - Create / set up .env file in project folder (see section named "Setting up .env")

- Running the backend:
    - Run: python gemini/app.py

- Running the frontend:
    - Open a new terminal
    - Run: start front-end.html

### For macOS:
- In root folder run:
    - python3 -m venv venv
    - source venv/bin/activate
    - ./venv/bin/pip install -r requirements.txt
        - If there is a notice saying to update pip, copy the command and paste it in terminal to update pip.
    - ./venv/bin/pip install pillow
    - Create / set up .env file in project folder (see section named "Setting up .env")

- Running the backend:
    - Run: ./venv/bin/python gemini/app.py

- Running the frontend:
    - Open a new terminal
    - Run: open front-end.html