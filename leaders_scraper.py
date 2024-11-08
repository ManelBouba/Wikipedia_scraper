# 10 lines
import requests
from bs4 import BeautifulSoup
import re
import json
def get_new_cookies(cookie_url):
    cookies = requests.get(cookie_url).cookies.get_dict()
    return cookies

def get_first_paragraph(wikipedia_url,session):
    # Extract language and title from the URL
    match = re.search(r"https://([a-z]+)\.wikipedia\.org/wiki/(.+)", wikipedia_url)
    if not match:
        return ""
    
    language = match.group(1)
    title = match.group(2)

    api_url = f"https://{language}.wikipedia.org/api/rest_v1/page/summary/{title}"
    response = requests.get(api_url)
    if response.status_code != 200:
        return ""
    
    data = response.json()
    return data.get("extract", "")

def get_leaders():
    # Define the URLs
    leaders_url = 'https://country-leaders.onrender.com/leaders'
    countries_url = 'https://country-leaders.onrender.com/countries'
    cookie_url = 'https://country-leaders.onrender.com/cookie'
    
    # Get the cookies
    cookies = get_new_cookies(cookie_url)
    
    # Get the countries
    countries = requests.get(countries_url, cookies=cookies).json()
    session = requests.Session()
    # Loop over countries and get the leaders
    leaders_per_country = {}
    for country in countries:
        response = requests.get(leaders_url, cookies=cookies, params={'country': country})
        leaders = response.json()
        # Store the leaders' first paragraphs
        leaders_per_country[country] = {}
        cookies = get_new_cookies(cookie_url)
        for leader_info in leaders:
            if type(leader_info)==dict:
            # Combine first and last names to get the full name
                leader_name = f"{leader_info.get('first_name')} {leader_info.get('last_name')}"
                wikipedia_url = leader_info.get('wikipedia_url')
                if wikipedia_url:
                    first_paragraph = get_first_paragraph(wikipedia_url,session)
                    print(first_paragraph)
                    leaders_per_country[country][leader_name] = first_paragraph
                    print(f"Leader: {leader_name}, Country: {country}, First Paragraph: {first_paragraph}")
    
    return leaders_per_country

def save_leaders_to_json(filename='leaders.json'):
    # Get leaders data
    leaders_per_country = get_leaders()
    
    # Write to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=4)
    
    print(f"Leaders data has been written to {filename}.")

# Example usage
save_leaders_to_json()


