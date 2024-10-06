import requests
import bs4
import re

webpage = requests.get("https://godotengine.org/asset-library/asset?max_results=50&page=0&filter=&category=&godot_version=&cost=&sort=updated", timeout=60)
webpage.raise_for_status()
soup = bs4.BeautifulSoup(webpage.text, 'html.parser')
# Find all asset items
assets = soup.find_all('li', class_='asset-item')

# List to hold asset data
asset_data = []
main_page_data = {}
total_assets = int(re.findall(pattern="\d+", string=str(soup.find("div", class_="pagination-stats").find_all("div")[1].text))[1])
max_pages = soup.find("ul", class_="pagination").find_all("li")[-2].find_all("a")[0].text

main_page_data['total'] = total_assets
main_page_data['max_pages'] = int(max_pages)

# Extract and store asset information in the list
for asset in assets:
    title = asset.find('h4').text  # Asset name
    url = "https://godotengine.org" + asset.find('a', class_='asset-header')['href']  # Asset URL
    img_url = asset.find('img', class_='media-object')['src']  # Image URL
    img_alt = asset.find('img', class_='media-object')['alt']  # Image alt text
    user = asset.find('div', class_='asset-footer').find('a').text  # User
    user_url = "https://godotengine.org/asset-library/asset" + asset.find('div', class_='asset-footer').find('a')['href']  # User URL
    version = asset.find('div', class_='asset-footer').find('b').text  # Version
    date = asset.find('div', class_='asset-footer').find('span').text.split('|')[-1].strip()  # Date
    project_license = ""
    godot_version = ""
    project_type = ""
    support_level = ""
    tags = []
    for tag_container in asset.find_all('div', class_='asset-tags'):
        for tag in tag_container.find_all('span'):
            tags.append(tag.text)


    project_type = tags[0]
    godot_version = tags[1]
    project_license = tags[3]
    support_level = tags[2]


    # Append the extracted data as a dictionary to the list
    asset_data.append({
        'title': title,
        'url': url,
        'img_url': img_url,
        'img_alt': img_alt,
        'user': user,
        'user_url': user_url,
        'version': version,
        'date': date,
        'license': project_license,
        'type': project_type,
        'godot_version': godot_version,
        'support_level': support_level
    })

# Print the list of asset data
print(
    {
        'main_page_data': main_page_data,
        'assets': asset_data
    }
)

