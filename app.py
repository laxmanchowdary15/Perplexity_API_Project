from flask import Flask, render_template, request, Response
import os
from openai import OpenAI
from fpdf import FPDF  # fpdf2 is imported the same way
import io

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

def generate_paper(subject, chapter, difficulty):
    prompt = (f"Create a model paper for class 10 {subject}, "
              f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
              "C (2x4), D (1x4), with suitable questions. Output in plain text, easy to print.")
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_exam_pdf(text, subject, chapter):
    pdf = FPDF()
    pdf.add_page()

    # Add a Unicode capable TTF font - DejaVuSans is a good free font
    # Make sure you have 'DejaVuSans.ttf' in a 'fonts' folder or same folder as app.py
    pdf.add_font('DejaVu', '', 'static/fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=12)

    header = f"Class 10 Model Paper - {subject} - {chapter}"
    pdf.cell(0, 10, header, ln=1, align="C")
    pdf.ln(5)

    # Write all lines, supporting UTF-8 characters
    for line in text.split('\n'):
        pdf.multi_cell(0, 8, line)

    # Return PDF as bytes directly (no encode needed)
    return pdf.output(dest='S').encode('latin1')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        difficulty = request.form['difficulty']

        paper_text = generate_paper(subject, chapter, difficulty)

        pdf_content = create_exam_pdf(paper_text, subject, chapter)

        pdf_stream = io.BytesIO(pdf_content)
        pdf_stream.seek(0)
        data = pdf_stream.read()

        response = Response(data, mimetype='application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=f"{subject}_{chapter}_model_paper.pdf")
        response.headers['Content-Length'] = len(data)
        return response

    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
