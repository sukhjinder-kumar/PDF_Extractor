- Activate or create a new virtual environment using `python -m venv /path/to/new/virtual/environment` and `source /path/to/new/virtual/environment/bin/activate`

- Install dependencies using `pip install -r requirements.txt`

- Create a `.env` file like following and change username and password to your email id and password. Note for a gmail client, you need to share app password! 

```.env
username="your_email@provider.com"
password="your_password"
target_header="Your target header you want to query upon"
```

- Just run the file `python gmail_extractor.py`, your attachements will be downloaded in `Attachements/` folder

- Than run the file `python pdf_extractor.py`, it will save your images and parsed text into Output folder

- Finally `python transaction_parser.py` to extract trasactional information from text output.
