# Bazos Real Estate Scraper

This repository contains a Python script for scraping real estate listings from the Bazos website. The script uses `requests` to make HTTP requests, `BeautifulSoup` for parsing HTML content, `pandas` for data manipulation, and `sqlalchemy` for database interaction.

## Features

- Scrape real estate listings from Bazos.
- Extract details such as links, titles, descriptions, prices, and locations.
- Save the data to a pandas DataFrame.
- Export the data to an Excel file.
- Create a PostgreSQL table and insert the data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Pip (Python package installer)
- PostgreSQL server running

## Requirements

- `Python 3`
- `requests`
- `beautifulsoup4`
- `pandas`
- `sqlalchemy`
- `PostgreSQL database`

## Installation

To install the required Python packages, run the following command:

```bash
pip install requests beautifulsoup4 pandas sqlalchemy
```

## Usage

To use the Bazos scraper, follow these steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/bazos-scraper.git
cd bazos-scraper
```

2. Update the `BASE_URL`, `category_url`, and `start_page` variables in the script to match your desired scraping parameters.

3. Run the script:

```bash
python bazos_scraper.py
```

The script will start scraping the website and save the data to an Excel file and a PostgreSQL database.

## Example
```
# Define the base URL and category URL for scraping.
BASE_URL = 'https://reality.bazos.cz'
category_url = 'https://reality.bazos.cz/prodam/byt/'
start_page = 7000

# Create an instance of the scraper.
scraper = BazosScraper(BASE_URL, category_url, start_page)
current_date = datetime.datetime.now().strftime("%d-%m-%Y")

# Extract data and convert it to a DataFrame.
data = scraper.extract_all_data()
df = scraper.make_dataframe(data)

# Save the DataFrame to an Excel file.
df.to_excel(f'scrape bazos/bazos_prodam_byt_{current_date}.xlsx', index=False)

# Create a PostgreSQL table with the scraped data.
BazosScraper.create_postgre_table(current_date, df)
```
## Contributing to Bazos Real Estate Scraper

To contribute to Bazos Real Estate Scraper, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## Contact

If you want to contact me you can reach me at `peterkacmarik@gmail.com`.

## License

This project uses the following license: `MIT`.

**Note:**

This script is for educational purposes only. Be mindful of Daft.ie's terms of service when scraping their website.
