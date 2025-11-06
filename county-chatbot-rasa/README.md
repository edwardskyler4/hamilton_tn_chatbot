County Chatbot (Rasa) - Ready to Run Locally
===========================================

Project structure:
county-chatbot-rasa/
├── data/
│   ├── nlu.yml
│   ├── stories.yml
│   ├── intents.csv
│   ├── intents_bilingual.json
├── domain.yml
├── config.yml
├── endpoints.yml
├── actions/
│   └── actions.py
├── scripts/
│   └── run_local.sh
├── requirements.txt
└── README.md

How to run (locally):
1. Install Python 3.8+ and create a virtual environment:
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows (PowerShell)

2. Install the dependencies:
   pip install -r requirements.txt

3. Train the Rasa model:
   rasa train

4. In one terminal, start the actions server:
   rasa run actions

5. In another terminal, run Rasa:
   rasa run --enable-api

6. Test the bot locally:
   rasa shell

Notes:
- The nlu.yml contains English and Spanish examples for each intent under the same tag.
- Responses are defined in domain.yml (both English and Spanish variants are present).
- Expand training data by editing data/nlu.yml or data/intents_bilingual.json.
