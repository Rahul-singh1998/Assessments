import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

def extract_books_info(url):
    
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    SAVE_CSV = os.path.join(base_dir, "Books.csv")
    final_result = []

    try:
        # Loop through paginated pages
        for i in range(1, 11):
            paginated_url = f"{url}catalogue/page-{i}.html"

            try:
                # Send HTTP request to the page
                response = requests.get(paginated_url)
                response.raise_for_status()  # Raise error for bad responses
            except Exception as e:
                print(f"Request failed for page {i}: {e}")
            else:
                print(f"Page: {i} | Status Code: {response.status_code}")

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.content, "html.parser")

                # Each book is inside an <li> under <ol class="row">
                rows = soup.find('ol', class_='row').find_all('li')

                # Extract data for each book
                for li in rows:
                    title = li.find('h3').text.strip()
                    price = li.find('p', class_="price_color").text.strip()
                    availability = li.find('p', class_="instock availability").text.strip()
                    rating_tag = li.find("p", class_="star-rating")
                    rating = "Unknown"
                    if rating_tag:
                        for c in rating_tag.get("class", []):
                            if c != "star-rating":
                                rating = c
                                break

                    # Store extracted data in dictionary format
                    disc = {
                        "Title": title.replace('.', ''),
                        "Price": price,
                        "Availability": availability,
                        "Rating": rating
                    }

                    # Add the record to the final results list
                    final_result.append(disc)

    except Exception as e:
        print(f"Unexpected error during scraping: {e}")

    finally:
        # Convert results to a DataFrame and save as CSV
        try:
            df = pd.DataFrame(final_result)
            df.to_csv(SAVE_CSV, index=False, encoding="utf-8-sig")
            print(f"CSV saved at: {SAVE_CSV}")
        except Exception as e:
            print(f"Failed to save the CSV: {e}")


# Start scraping from the base URL
extract_books_info(BASE_URL)
