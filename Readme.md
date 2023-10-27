# Getting Started
Follow these steps to run the program -

1. Activate or create a new virtual environment using `python -m venv Env` and `source Env/bin/activate`

2. Install dependencies using `pip install -r requirements.txt`

3. Create a `.env` file which contains following. Change username and password to your email id and password. Note for a gmail client, you need to share app password!

```.env
username="your_email@gmail.com"
password="your_password"
target_header="Your target header you want to query upon"
```

There is an included attachement inside the `Attachement/` folder, so you don't need to run this step to test the remaining codebase.

4. Run the file `python gmail_extractor.py`, your attachements will be downloaded in `Attachements/` folder. It searches for messages that has `target_header` as the subject and contains `.pdf` attachement.

Now you can either use the api's created in `api.py` file (first host it) or use exact function defined in various files.
Demo on how to use api's is provided in file `test_api.py`.

5. Run the file `python pdf_extractor.py`, it will save your images and parsed text into Output folder. Change the `pdf_path` variable in the file!

6. Finally run `python transaction_parser.py` to extract trasactional information from text output.

## Here are the api's

1. `/filter_transaction`: Takes text and Returns a list of Transaction objects (class of 3 attributes, date which is a datetime object, client (str), amount (float)). It parses the text, and find lines that match the pattern `<mm/dd/yyyy> <string> <amount>`. As class can't be json serialized, it is converted into a dict and returned. So care must be made while interpretating the output.

2. `/total_transactional_cost`: Takes transactions as input and return total amount. The output is a string, so use float(output) to typecast into float. Note transactions as is made up of classes and can't be passed directly to api, conversion into dict must be done. See test_api file to see how we did there. It is exact same as response given by filter_transaction api.

3. `/transactional_cost_timeframe`: Takes transactions, intial_date, and end_date as input and return amount spent during that duration. Here to output is str and typecasting is needed to convert into float.

Note that though tempting to generalize the code to any bank statement, it best works on bank statements of form similar to one inside `Attachement\` folder
