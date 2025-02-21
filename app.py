from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF for PDF text extraction
import tensorflow as tf
import pickle
import numpy as np
import re
import os

# Load the trained model
model = tf.keras.models.load_model("model/resume_classification_model.h5")

# Load the TF-IDF Vectorizer
with open("model/tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer = pickle.load(f)

# Load the Label Encoder
with open("model/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    text = re.sub(r'\d+', ' ', text)  # Remove digits
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

@app.route("/", methods=["GET", "POST"])
def upload_resume():
    if request.method == "POST":
        if "resume" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            # Extract text from PDF
            resume_text = extract_text_from_pdf(file_path)

            if not resume_text:
                return jsonify({"error": "Could not extract text from PDF"}), 400

            # Preprocess and predict
            cleaned_resume = clean_text(resume_text)
            resume_tfidf = tfidf_vectorizer.transform([cleaned_resume]).toarray()
            prediction = model.predict(resume_tfidf)
            predicted_category = label_encoder.inverse_transform([np.argmax(prediction)])[0]

            return render_template("result.html", category=predicted_category, text=resume_text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
