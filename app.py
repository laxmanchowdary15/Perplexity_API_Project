from flask import Flask, render_template, request, send_file
import os
from openai import OpenAI
from fpdf import FPDF
import io

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

def generate_paper(subject, chapter, difficulty):
    prompt = (f"Create a 30-mark model paper for class 10 {subject}, "
              f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
              "C (2x4), D (1x4), with suitable questions. Output in print-friendly text.")
    response = client.chat.completions.create(
        model="pplx-7b-chat",  # <-- updated here
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        difficulty = request.form['difficulty']
        paper = generate_paper(subject, chapter, difficulty)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in paper.split('\n'):
            pdf.cell(0, 10, line, ln=1)
        pdf_stream = io.BytesIO(pdf.output(dest='S').encode('latin-1'))
        pdf_stream.seek(0)
        return send_file(pdf_stream, as_attachment=True,
                         download_name="model_paper.pdf", mimetype='application/pdf')
    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
