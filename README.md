Capstone Project - Mad Men and Machines

There is a .venv folder included for the libraries that are needed

==== Data ====

In this folder there are multiple excel sheets where the ads, texts, links and annotations are stored.
create_csv.py creates a csv file for a classifier to train on from the all_text_ads sheet.

==== Scraper ====

The scripts in this folder are used as tools to scrape ad content from the meta ad library. In order for them to run, you need a driver to interface with the browser (https://sites.google.com/chromium.org/driver/). The working of these scripts are dependent on browser settings and might not produce the same results. These scripts were mostly used as tools and some manual work was required to get a proper dataset.

==== Annotation ====

These scripts use the LLM to annotate the ad data. For them to work an API key is needed. The API key for Chat-GPT needs to be set as the environmental variable OPENAI_API_KEY. The API key for Claude needs to be set as the environmental variable ANTHROPIC_API_KEY. If you need the API keys to test the code let us know, then we will ask the client if that is okay. 

==== Analysis ====

In this folder there are scripts to evaluate the dataset, for example bias and inter-coder reliability.
