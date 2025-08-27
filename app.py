from flask import Flask, render_template, request, send_file
import os
from openai import OpenAI
from fpdf import FPDF
import io

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")

def generate_paper(subject, chapter, difficulty):
    prompt = (f"Create a model paper for class 10 {subject}, "
              f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
              "C (2x4), D (1x4), with suitable questions. Output in print-friendly text.")
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

class PDF(FPDF):
    def header(self):
        pass  # no default header
    
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 10)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def create_exam_pdf(text, subject, chapter):
    pdf = PDF()
    pdf.add_page()
    
    # Add DejaVu font for Unicode support
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", 'B', 16)

    header = f"Class 10 Model Paper - {subject} - {chapter}"
    pdf.cell(0, 10, header, ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("DejaVu", '', 12)
    pdf.set_auto_page_break(auto=True, margin=15)

    for line in text.split('\n'):
        pdf.multi_cell(0, 8, line)

    pdf_output = pdf.output(dest='S').encode('latin-1', errors='ignore')
    return pdf_output

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

        return send_file(
            pdf_stream,
            as_attachment=True,
            download_name=f"{subject}_{chapter}_model_paper.pdf",
            mimetype='application/pdf',
            conditional=True
        )
    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
