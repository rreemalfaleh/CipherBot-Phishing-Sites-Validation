# Cipher-BOT: Validation of Phishing Sites Using AI 

## Overview

This repository contains a Python script that automates the process of validating phishing sites. It utilizes various technologies and APIs to capture screenshots, perform logo detection, analyze content, and compare images for similarity. The script is designed to aid in the identification of potential phishing sites, making the validation process more efficient.

## Instructions

Follow these steps to use the code:

1. Clone the repository to your local machine:

    ```bash
    https://github.com/rreemalfaleh/CipherBot-Phishing-Sites-Validation.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up a service account key for [Google Cloud Vision API](https://cloud.google.com/vision?hl=en) and replace the placeholder in `YOUR PATH\KEY.json` with the actual path to your key file.

4. Obtain an API key from [DeepAI](https://deepai.org/machine-learning-model/image-similarity) and replace the placeholder `'YOUR API KEY'` in `app.py` with your actual API key.

5. **Download ChromeDriver:**
    - ChromeDriver is not a Python package and needs to be downloaded separately.
    - Visit the [ChromeDriver download page](hhttps://chromedriver.chromium.org/) and download the appropriate version for your operating system.
    - Extract the downloaded archive and ensure the `chromedriver` executable is available in your system's PATH.

6. Run the script:

    ```bash
    python app.py
    ```

## Note

This repository was created for educational purposes and to demonstrate automated phishing site validation. It is crucial to use such tools responsibly and ethically. The script should not be used for any malicious or unethical activities.

## Disclaimer

This repository and its content were used for a presentation at Black Hat Middle East and Africa (Riyadh, KSA). The intention is solely educational, and users are responsible for adhering to ethical standards and legal regulations.


