import requests
from bs4 import BeautifulSoup

# Prompt the user for the 1337x.to link
link = input("Enter the 1337x.to link: ")

# Send a GET request to the link and retrieve the HTML content
response = requests.get(link)
html_content = response.content

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the name
name = soup.find('div', class_='box-info-heading').find('h1').text.strip()

# Extract the description (with error handling)
description_element = soup.find('div', class_='box-info-description')
description = description_element.text.strip() if description_element else 'No description available.'

# Extract the magnet link
magnet_link = soup.find('a', class_='lc5ee1ede109dea8c348ff76dcc09ac21a845e57e').get('href')

# Extract the torrent link
torrent_link = soup.find('a', class_='lc5ee1ede109dea8c348ff76dcc09ac21a845e57e', target='_blank').get('href')

# Extract the stream button link (if available)
stream_button = soup.find('a', id='lf5d2f65a9a82ac814de9337f2a06c6030e49bd38')
stream_link = stream_button.get('href') if stream_button else 'No stream link available.'

# Print the extracted information
print("Name:", name)
print("Description:", description)
print("Magnet Link:", magnet_link)
print("Torrent Link:", torrent_link)
print("Stream Link:", stream_link)
