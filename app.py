from flask import Flask, render_template, request, Response
from flask import make_response
import os
from openai import OpenAI
from fpdf import FPDF
from fpdf.enums import XPos, YPos

import re

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

# -------------------- Generate Paper --------------------
def generate_paper(subject, chapter, difficulty,suggestions):
    prompt = (
        f"Create a model paper for class 10 {subject}, "
        f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
        "C (2x4), D (1x4), with suitable questions. Some extra suggestions are "
        + suggestions + " "
        "Use plain text and clean mathematical symbols. "
        "Avoid LaTeX, avoid \\( \\), avoid $$. Use superscripts (x²), fractions (a/b), etc. "
        "Make questions strictly based difficulty level but add one difficult question in all levels. "
        "Follow the questions format and syllabus of Andhra Pradesh board for all classes and formats. "
        "Give response as exam question paper no hint or extra descriptions in response of any kind, "
        "since response is being printed as pdf."
    )
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_exam_pdf(text, subject, chapter):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    # Load Unicode font
    font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'DejaVuSans.ttf')
    pdf.add_font("DejaVu", "", font_path)
    pdf.add_font("DejaVu", "B", font_path)
    pdf.add_font("DejaVu", "I", font_path)

    page_width = pdf.w - 2 * pdf.l_margin

    # Header
    pdf.set_font("DejaVu", "B", 16)
    header = f"Class 10 Model Paper - {subject} - {chapter}"
    pdf.cell(0, 12, header, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(10)

    # Body
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue

        if line.startswith("**Section"):
            section_title = line.replace("**", "")
            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(0, 10, section_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(3)
        else:
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(page_width, 7.5, line)
            pdf.ln(0.5)

    # Footer
    pdf.ln(5)
    pdf.set_font("DejaVu", "I", 12)
    pdf.cell(0, 10, "*End of Paper*", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    return bytes(pdf.output(dest="S"))

# -------------------- Routes --------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        difficulty = request.form['difficulty']
        suggestions = request.form.get('suggestions', '')

        paper_text = generate_paper(subject, chapter, difficulty, suggestions)
        pdf_content = create_exam_pdf(paper_text, subject, chapter)

        response = make_response(pdf_content)
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=f"{subject}_{chapter}.pdf")
        return response

    return render_template('form.html')

# -------------------- Run --------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
