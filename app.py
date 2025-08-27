from flask import Flask, render_template, request, Response
import os
from openai import OpenAI
from fpdf import FPDF
import io

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

def generate_paper(subject, chapter, difficulty):
    prompt = (f"Create a model paper for class 10 {subject}, "
              f"chapter '{chapter}', difficulty: {difficulty}. "
              "Structure it as Section A (10x1 marks), Section B (4x2 marks), "
              "Section C (2x4 marks), Section D (1x4 marks) with suitable questions. "
              "Output in plain text, easy to print.")
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_exam_pdf(text, subject, chapter):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=12)

    header = f"Class 10 Model Paper - {subject} - {chapter}"
    pdf.cell(0, 10, header, ln=1, align="C")
    pdf.ln(5)

    for line in text.split('\n'):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest='S').encode('latin-1', 'replace')

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
