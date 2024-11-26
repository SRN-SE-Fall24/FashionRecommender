import requests
import urllib.parse
import os
import re

# GitHub API URL for the repository languages
url = f'https://api.github.com/repos/SRN-SE-Fall24/FashionRecommender/languages'

# Send GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    languages = response.json()

    # Calculate total lines of code to determine percentages
    total_lines = sum(languages.values())

    # Generate badge markdown
    badges = []
    for language, lines in languages.items():
        percentage = (lines / total_lines) * 100
        percentage = round(percentage, 2)  # Round to 2 decimal places

        # Create a badge URL using Shields.io
        badge_url = f'https://img.shields.io/badge/{urllib.parse.quote(language)}-{percentage}%25-blue'
        badges.append(f'![{language}]({badge_url})')

    # Read the current README.md file
    with open('README.md', 'r', encoding='utf-8', errors='replace') as readme_file:
        readme_content = readme_file.read()

    # Update the README with the new badges
    #<!-- Start marker for language badge generation -->
    #<!-- End marker for language badge generation -->
    marker1 = re.escape('<!-- Start marker for language badge generation -->')
    marker2 = re.escape('<!-- End marker for language badge generation -->')
    updated_readme_content = re.sub(
        rf'{marker1}.*?{marker2}', 
        '<!-- Start marker for language badge generation -->' + '\n' + '\n'.join(badges) + '\n' + '<!-- End marker for language badge generation -->', 
        readme_content, 
        flags=re.DOTALL)
    
    # Write the updated content back to the README.md file
    with open('README.md', 'w', errors='replace') as readme_file:
        readme_file.write(updated_readme_content)

else:
    print("Error fetching data:", response.status_code)
