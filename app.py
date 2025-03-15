import requests
from flask import Flask, render_template, request, send_file
import io
from PIL import Image as PILImage
import google.generativeai as genai
import random

# Configure Gemini API
GEMINI_API_KEY = "Your_gemini_api_key"  # Your API key
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

# Function to get meme template IDs from Memegen.link API
def get_meme_template_ids():
    url = "https://api.memegen.link/templates"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            templates = response.json()
            return [template['id'] for template in templates]
        else:
            print(f"Failed to fetch templates. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching templates: {e}")
        return ['buzz', 'doge', 'fry', 'pigeon', 'drake']  # Fallback templates

# Function to generate meme text using Gemini API
def generate_meme_text(context):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Given the context: '{context}'
    Generate two short, funny lines for a meme. Return them as a list with exactly two strings:
    - First string: Top text
    - Second string: Bottom text
    Keep it concise and humorous!
    Example output: ["WHEN YOU FINALLY", "GET REVENGE"]
    """
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1].replace('```', '').strip()
        lines = text[1:-1].split(',')[:2] if text.startswith('[') else text.split('\n')[:2]
        return [line.strip().strip('"') for line in lines]
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        return ["GEMINI BROKE", "SEND HELP"]

# Function to generate meme URLs and shuffle them
def generate_meme_urls(template_ids, top_text, bottom_text):
    BASE_URL = "https://api.memegen.link/images/"
    meme_data = []
    top = top_text.replace(" ", "_")
    bottom = bottom_text.replace(" ", "_")
    
    for template in template_ids:
        url = f"{BASE_URL}{template}/{top}/{bottom}.png"
        meme_data.append({"template": template, "url": url})
    
    random.shuffle(meme_data)  # Shuffle the order
    return meme_data

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        context = request.form['context']
        template_ids = get_meme_template_ids()
        top_text, bottom_text = generate_meme_text(context)
        memes = generate_meme_urls(template_ids, top_text, bottom_text)
        return render_template('index.html', memes=memes, context=context)
    return render_template('index.html', memes=None)

@app.route('/download/<template>/<top>/<bottom>')
def download_meme(template, top, bottom):
    url = f"https://api.memegen.link/images/{template}/{top}/{bottom}.png"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Open and crop the image
            img = PILImage.open(io.BytesIO(response.content))
            width, height = img.size
            crop_height = int(height * 0.85)  # Crop bottom 15% to remove watermark
            cropped_img = img.crop((0, 0, width, crop_height))
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            cropped_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name=f"{template}_meme.png")
        else:
            return f"Error fetching meme: Status {response.status_code}", 500
    except Exception as e:
        print(f"Error in download: {e}")
        return "Error generating meme", 500

if __name__ == '__main__':
    app.run(debug=True)
