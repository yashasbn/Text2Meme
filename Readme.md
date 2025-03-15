# Text2Meme

Text2Meme is a Python-based web application that allows you to generate memes by adding custom text to images. It uses the Gemini API to generate captions automatically.

## Requirements

Make sure you have Python 3.x installed. You will also need to install the required dependencies.

## Installation

1. Clone the repository or download the ZIP file and extract it.

2. Navigate to the project directory:
    ```bash
    cd Text2Meme
    ```

3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the web application locally, use the following command:
    ```bash
    python app.py
    ```

By default, the app will start on `http://127.0.0.1:5000/`.

## Gemini API Integration

This application uses the **Gemini API** to automatically generate captions for your meme images. To use this feature, you'll need to replace the **Gemini API key** in the `app.py` file.

### Steps to Replace the API Key:

1. Sign up for an account on the Gemini platform (if you don’t have one already).
   
2. After signing in, obtain your Gemini API key from the [Gemini API & Services](https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com).

3. Open the `app.py` file in your project directory.

4. Look for the line where the API key is used, which will look something like this:
    ```python
    GEMINI_API_KEY = 'Your_gemini_api_key'
    ```

5. Replace `'Your_gemini_api_key'` with your actual Gemini API key.

6. Save the changes to `app.py`.

## Folder Structure

- **app.py**: The main Python file that runs the application.
- **requirements.txt**: Lists all the Python dependencies needed for the project.
- **static/**: Contains static files like images, JavaScript, and CSS files.
- **templates/**: Contains HTML files for the web pages.

## Usage

1. Open your web browser and go to `http://127.0.0.1:5000/`.
2. Upload an image and enter the text you want to appear on the meme.
3. Adjust the text position and size if needed.
4. Click on the "Generate Meme" button to create the meme.
5. Download or share your meme as needed.

