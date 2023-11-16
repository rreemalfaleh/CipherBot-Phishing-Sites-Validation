import os
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from google.cloud import vision_v1
from skimage.metrics import structural_similarity as ssim
from bs4 import BeautifulSoup
import requests
import re
import jsbeautifier

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')

# Initialize the headless browser
browser = webdriver.Chrome(options=chrome_options)

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"YOUR-PATH\KEY.json"

# Set up the Google Cloud Vision client
client = vision_v1.ImageAnnotatorClient()

# DeepAI API key
api_key = 'YOUR API KEY'

# Capture a screenshot function
def capture_screenshot(url, filename='screenshot.png'):
    # Navigate to the URL
    browser.get(url)

    # Capture a screenshot
    browser.save_screenshot(filename)

# Logo detection function using Google Cloud Vision API
def detect_logo(image_path):
    # Read the image file
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an image object
    image = vision_v1.Image(content=content)

    # Perform logo detection
    response = client.logo_detection(image=image)

    # Print detected logos
    for logo in response.logo_annotations:
        print(f'Detected Logo: {logo.description}, Score: {logo.score}')

# Content analysis function
def analyze_content(url):
    try:
        # Retrieve HTML content of the web page
        response = requests.get(url)
        html_content = response.text

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Perform content analysis
        # Check for login forms
        login_forms = soup.find_all('form', {'action': re.compile(r'(login|signin)', re.IGNORECASE)})
        if login_forms:
            print("Potential phishing: Login form detected")

        # Check for suspicious URLs
        suspicious_urls = soup.find_all('a', href=re.compile(r'(login|signin|phishing)', re.IGNORECASE))
        if suspicious_urls:
            print("Potential phishing: Suspicious URLs detected", url)

        # Check for obfuscated JavaScript
        scripts = soup.find_all('script')
        for script in scripts:
            js_code = script.get_text()
            beautified_js = jsbeautifier.beautify(js_code)
            if 'eval(' in beautified_js:
                print("Potential phishing: Obfuscated JavaScript detected")

        # Check meta tags for inconsistencies
        meta_tags = soup.find_all('meta')
        for meta_tag in meta_tags:
            if 'keywords' in meta_tag.attrs and 'description' in meta_tag.attrs:
                keywords = meta_tag['keywords']
                description = meta_tag['description']
                if keywords.lower() in description.lower():
                    print("Potential phishing: Meta tags inconsistency detected")

        # Check for iframes
        iframes = soup.find_all('iframe')
        if iframes:
            print("Potential phishing: Iframes detected")

    except Exception as e:
        print(f"Error analyzing content: {e}")

# Image similarity comparison using DeepAI API
def compare_images(image_path1, image_path2):
    with open(image_path1, 'rb') as image_file1, open(image_path2, 'rb') as image_file2:
        files = {
            'image1': ('legitimate_screenshot.png', image_file1),
            'image2': ('malicious_screenshot.png', image_file2),
        }

        headers = {'api-key': api_key}

        r = requests.post("https://api.deepai.org/api/image-similarity", files=files, headers=headers)

    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error {r.status_code}: {r.text}")
        return None

# SAMPLE: Capture a screenshot of a malicious URL
malicious_url = 'https://earnings-sci-presentations-potato.trycloudflare.com/login.html.php'
capture_screenshot(malicious_url, 'malicious_screenshot.png')

legitimate_url = 'https://www.netflix.com/sa-en/login'
capture_screenshot(legitimate_url, 'legitimate_screenshot.png')

# Content analysis for the malicious URL
analyze_content(malicious_url)

# Example: Detect logo in the malicious screenshot using Google Cloud Vision API
detect_logo('malicious_screenshot.png')

# Example: Compare images using DeepAI API
similarity_result = compare_images('legitimate_screenshot.png', 'malicious_screenshot.png')
if similarity_result:
    print(f"Image Similarity Score: {similarity_result['output']['distance']}")

# Close the browser
browser.quit()
