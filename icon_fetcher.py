import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

def fetch_program_icon(program_name):
    try:
        # Fetch the Chocolatey package page
        url = f"https://community.chocolatey.org/packages/{program_name}"
        print(f"Fetching icon from URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Find the version number
            version_tag = soup.find('span', class_='package-version')
            if version_tag:
                version = version_tag.text.strip()
                print(f"Found version: {version}")
                # Construct the icon URL
                icon_url = f"https://community.chocolatey.org/content/packageimages/{program_name}.{version}.png"
                print(f"Constructed icon URL: {icon_url}")
                icon_response = requests.get(icon_url)
                if icon_response.status_code == 200:
                    print(f"Successfully fetched icon from URL: {icon_url}")
                    return Image.open(BytesIO(icon_response.content))
                else:
                    print(f"Failed to fetch icon from URL: {icon_url}, status code: {icon_response.status_code}")
            else:
                print(f"Failed to find version for {program_name}")
            print(f"Failed to find specific icon for {program_name}, using placeholder icon.")
        else:
            print(f"Failed to fetch Chocolatey page, status code: {response.status_code}")
        # Fallback to placeholder icon
        return create_placeholder_icon(program_name)
    except Exception as e:
        print(f"An error occurred while fetching the icon: {e}")
        return create_placeholder_icon(program_name)

def create_placeholder_icon(program_name):
    # Create a placeholder image
    placeholder = Image.new('RGB', (100, 100), color=(73, 109, 137))
    draw = ImageDraw.Draw(placeholder)
    try:
        # Use a truetype font if available
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        # Use a default bitmap font if truetype is not available
        font = ImageFont.load_default()
    text = program_name[0].upper()  # Use the first letter of the program name
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((100 - text_width) / 2, (100 - text_height) / 2)
    draw.text(position, text, fill=(255, 255, 255), font=font)
    return placeholder