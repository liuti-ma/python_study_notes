import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape (Allrecipes' main page for recipes)
url = "https://www.allrecipes.com/recipes/"

# Send a GET request to the website
response = requests.get(url,verify=False)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all recipe cards
recipe_cards = soup.find_all('div', class_='card__detailsContainer')

# Initialize lists to store scraped data
recipe_names = []
ratings = []
prep_times = []

# Loop through each recipe card and extract data
for card in recipe_cards:
    # Extract recipe name
    name = card.find('span', class_='card__title').text.strip()
    recipe_names.append(name)

    # Extract rating (if available)
    rating_element = card.find('span', class_='review-star-text')
    if rating_element:
        rating = rating_element.text.strip().split()[1]  # Extract the numeric rating
    else:
        rating = "N/A"
    ratings.append(rating)

    # Extract preparation time (if available)
    prep_time_element = card.find('div', class_='card__summary')
    if prep_time_element:
        prep_time = prep_time_element.text.strip()
    else:
        prep_time = "N/A"
    prep_times.append(prep_time)

# Create a DataFrame to store the scraped data
data = {
    'Recipe Name': recipe_names,
    'Rating (out of 5)': ratings,
    'Preparation Time': prep_times
}
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('recipes.csv', index=False)

print("Scraping completed! Data saved to 'recipes.csv'.")