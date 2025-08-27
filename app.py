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
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

class ExamPaperPDF(FPDF):
    def header(self):
        self.set_font("Times", "B", 14)
        self.cell(0, 10, "Class 10 Model Question Paper", align="C", ln=1)
        self.ln(2)
    
    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        
    def chapter_title(self, title):
        self.set_font("Times", "B", 12)
        self.cell(0, 10, title, ln=1)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)
        
    def question(self, num, text):
        self.set_font("Times", "", 12)
        self.multi_cell(0, 8, f"{num}. {text}")
        self.ln(2)

def create_exam_pdf(paper_text, subject, chapter):
    pdf = ExamPaperPDF()
    pdf.add_page()
    
    pdf.chapter_title(f"Subject: {subject}    Chapter: {chapter}")
    
    lines = paper_text.strip().split('\n')
    question_num = 1
    for line in lines:
        line = line.strip()
        if not line:
            continue
        pdf.question(question_num, line)
        question_num += 1
    
    return pdf.output(dest='S').encode('latin-1')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        difficulty = request.form['difficulty']
        paper = generate_paper(subject, chapter, difficulty)

        pdf_content = create_exam_pdf(paper, subject, chapter)

        pdf_stream = io.BytesIO(pdf_content)
        pdf_stream.seek(0)
        filename = f"{subject}_{chapter}.pdf".replace(" ", "_")

        return send_file(pdf_stream, as_attachment=True,
                         download_name=filename,
                         mimetype='application/pdf')
    return render_template('form.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
