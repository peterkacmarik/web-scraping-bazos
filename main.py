import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import sqlalchemy
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError


class BazosScraper:
    """
    A scraper class to extract data from the Bazos website.
    
    Attributes:
        BASE_URL (str): The base URL of the Bazos website.
        category_url (str): The specific category URL to scrape.
        session (requests.Session): The session used for making HTTP requests.
        start_page (int): The starting page number for scraping.
    """
    
    def __init__(self, BASE_URL: str, category_url: str, start_page: int) -> None:
        """
        Initializes the BazosScraper with base URL, category URL, and start page.
        
        Args:
            BASE_URL (str): The base URL of the Bazos website.
            category_url (str): The specific category URL to scrape.
            start_page (int): The starting page number for scraping.
        """
        self.BASE_URL = BASE_URL
        self.category_url = category_url
        self.session = requests.Session()
        self.start_page = start_page
        
    def make_soup(self):
        """
        Makes a BeautifulSoup object from the category URL.
        
        Returns:
            BeautifulSoup: A BeautifulSoup object of the page content, or None if an error occurs.
        """
        try:
            # Construct the URL based on the current page number.
            if self.start_page == 0:
                url = self.category_url
            else:
                url = f'{self.category_url}{self.start_page}/'
            
            # Make an HTTP request and create a BeautifulSoup object.
            response = self.session.get(url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except RequestException as e:
            # Handle any request-related exceptions from the requests library
            print(f"An error occurred while making an HTTP request: {e}")
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f"An unexpected error occurred: {e}")
        return None  # Return None or an appropriate value if an error occurs

    def extract_all_data(self):
        """
        Extracts all relevant data from the category page.
        
        Returns:
            dict: A dictionary containing lists of data for each field, or None if an error occurs.
        """
        # Initialize a dictionary to store the scraped data.
        data = {
            'Links': [],
            'Titles': [],
            'Descriptions': [],
            'Prices': [],
            'Locations': []
        }
        
        try:
            # Continue scraping until there are no more advertisements.
            proceed = True
            while proceed:
                soup = self.make_soup()
                if soup is None:
                    print("Failed to retrieve data.")
                    return None
                
                start_point = soup.find('div', class_='maincontent')
                if start_point is None:
                    print("Could not find the starting point for data extraction.")
                    return None
                
                all_advertise = start_point.find_all('div', class_='inzeraty inzeratyflex')
                
                print(f'Current page: {self.start_page}')
                
                # Extract data from each advertisement.
                for item in all_advertise:
                    try:
                        data['Links'].append(self.BASE_URL + item.a['href'].strip())
                        data['Titles'].append(item.h2.text.strip())
                        data['Descriptions'].append(item.find_all('div', class_='popis')[0].text.strip())
                        data['Prices'].append(item.find_all('div', class_='inzeratycena')[0].text.replace('Kč', '').strip())
                        br_tag = item.find_all('div', class_='inzeratylok')[0]
                        br_tag.br.replace_with(', ')
                        data['Locations'].append(br_tag.text.strip())
                    except AttributeError as e:
                        print(f"An error occurred while extracting data from an advertisement: {e}")
                
                # Check if there are no more advertisements to scrape.
                if len(all_advertise) == 0:
                    proceed = False
                else:
                    self.start_page += 20  # Increment the page number.
        except Exception as e:
            print(f"An unexpected error occurred during data extraction: {e}")
            return None  # Return None or an appropriate value if an error occurs
        
        return data
        
    def make_dataframe(self, data_df: dict):
        """
        Converts the scraped data into a pandas DataFrame.
        
        Args:
            data_df (dict): The dictionary containing scraped data.
            
        Returns:
            DataFrame: A pandas DataFrame containing the scraped data.
        """
        try:
            # Check if the dictionary is empty
            if not data_df or not all(len(lst) == len(next(iter(data_df.values()))) for lst in data_df.values()):
                raise ValueError("Input dictionary is empty or values have inconsistent lengths.")
            
            # Convert the dictionary to a pandas DataFrame
            df = pd.DataFrame(data_df)
            return df
        except ImportError:
            print("Pandas library is not installed. Please install it using 'pip install pandas'.")
            return None
        except ValueError as e:
            print(f"An error occurred while creating DataFrame: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    @staticmethod    
    def create_postgre_table(current_date: str, df: pd.DataFrame):
        """
        Creates a PostgreSQL table with the scraped data.
        
        Args:
            current_date (str): The current date as a string.
            df (DataFrame): The pandas DataFrame containing the scraped data.
        """
        try:
            # Check if the DataFrame is empty
            if df.empty:
                raise ValueError("The DataFrame is empty and cannot be written to the database.")
            
            # Connect to the PostgreSQL database.
            engine = sqlalchemy.create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
            
            # Create a new table with the current date in its name.
            table_name = f'bazos_prodam_byt_{current_date}'
            df.to_sql(table_name, engine, if_exists='replace')
            print(f"Table '{table_name}' created successfully.")
        except ValueError as e:
            print(f"An error occurred: {e}")
        except SQLAlchemyError as e:
            print(f"An error occurred with the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # Define the base URL and category URL for scraping.
    BASE_URL = 'https://reality.bazos.cz'
    category_url = 'https://reality.bazos.cz/prodam/byt/'
    start_page = 7000

    # Create an instance of the scraper.
    scraper = BazosScraper(BASE_URL, category_url, start_page)
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")

    try:
        # Extract data and convert it to a DataFrame.
        data = scraper.extract_all_data()
        df = scraper.make_dataframe(data)
        # print(df)
        # Save the DataFrame to an Excel file.
        df.to_excel(f'scrape bazos/bazos_prodam_byt_{current_date}.xlsx', index=False)
        # Create a PostgreSQL table with the scraped data.
        BazosScraper.create_postgre_table(current_date, df)
    except ValueError as e:
        # Handle a ValueError specifically
        print(f"A ValueError occurred: {e}")
    except IOError as e:
        # Handle an IOError specifically
        print(f"An IOError occurred: {e}")
    except Exception as e:
        # Handle any other exceptions that weren't caught by the previous blocks
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the session after scraping is complete.
        scraper.session.close()