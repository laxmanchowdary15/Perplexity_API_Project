from flask import Flask, render_template, request, send_file
import os
from openai import OpenAI
from fpdf import FPDF
import io
import re

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

def sanitize_text(text):
    # Remove characters that can't be encoded in latin-1 (for FPDF)
    return text.encode('latin-1', errors='ignore').decode('latin-1')

def generate_paper(subject, chapter, difficulty):
    prompt = (f"Create a 30-mark model paper for class 10 {subject}, "
              f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
              "C (2x4), D (1x4), with suitable questions. Output in print-friendly text.")
    response = client.chat.completions.create(
        model="sonar-pro",  # Use your valid model here
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject'].strip()
        chapter = request.form['chapter'].strip()
        difficulty = request.form['difficulty']

        paper = generate_paper(subject, chapter, difficulty)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in paper.split('\n'):
            line = sanitize_text(line)
            pdf.cell(0, 10, line, ln=1)

        pdf_stream = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
        pdf_stream.seek(0)

        # Make filename safe by replacing spaces and non-alphanumeric with underscores
        safe_subject = re.sub(r'\W+', '_', subject)
        safe_chapter = re.sub(r'\W+', '_', chapter)
        filename = f"{safe_subject}_{safe_chapter}_model_paper.pdf"

        return send_file(pdf_stream, as_attachment=True,
                         download_name=filename, mimetype='application/pdf')

    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
