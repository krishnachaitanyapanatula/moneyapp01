import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pytesseract
from PIL import Image

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def signup():
    return render_template('signup.html')

# NEW: AJAX Route for Step 1
@app.route('/verify_ajax', methods=['POST'])
def verify_ajax():
    roll_no = request.form.get('roll_no')
    id_photo = request.files.get('id_photo')

    if not id_photo:
        return jsonify(success=False, message="No photo uploaded")

    filepath = os.path.join(UPLOAD_FOLDER, id_photo.filename)
    id_photo.save(filepath)

    try:
        extracted_text = pytesseract.image_to_string(Image.open(filepath))
        
        # Check if Roll No and College keyword are in the text
        if roll_no in extracted_text and 'IIITDM' in extracted_text:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Details not found on ID card.")
    except Exception as e:
        return jsonify(success=False, message=str(e))

# NEW: Final Route for Step 2
@app.route('/final_submit', methods=['POST'])
def final_submit():
    email = request.form.get('email')
    roll_no = request.form.get('roll_no')
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        return "Passwords do not match! Please go back."

    # Logic to save to database would go here
    return render_template('success.html', email=email, roll_no=roll_no, username=username)

if __name__ == '__main__':
    app.run(debug=True)