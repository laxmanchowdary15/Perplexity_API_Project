# from flask import Flask, render_template, request, Response
# import os
# from openai import OpenAI
# from fpdf import FPDF, XPos, YPos
# import io,re

# app = Flask(__name__)
# client = OpenAI(api_key=os.environ.get("PERPLEXITY_API_KEY"), base_url="https://api.perplexity.ai")
# def clean_math_latex(text):
#     # Replace \( ... \) or $ ... $ with inner content
#     text = re.sub(r"\\\((.*?)\\\)", r"\1", text)
#     text = re.sub(r"\$(.*?)\$", r"\1", text)
#     return text
# def generate_paper(subject, chapter, difficulty):
#     prompt = (
#         f"Create a model paper for class 10 {subject}, "
#         f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
#         "C (2x4), D (1x4), with suitable questions. Output in plain text, easy to print."
#     )
#     response = client.chat.completions.create(
#         model="sonar-pro",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content

# # def create_exam_pdf(text, subject, chapter):
# #     pdf = FPDF()
# #     pdf.add_page()

# #     pdf.set_margins(10, 10, 10)
# #     font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'DejaVuSans.ttf')
# #     pdf.add_font('DejaVu', '', font_path)  # Removed deprecated uni=True
# #     pdf.set_font("DejaVu", size=12)

# #     page_width = pdf.w - 2 * pdf.l_margin

# #     header = f"Class 10 Model Paper - {subject} - {chapter}"
# #     pdf.cell(0, 10, header, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")  # Updated ln param
# #     pdf.ln(5)

# #     for line in text.split('\n'):
# #         if line.strip() == "":
# #             pdf.ln(5)
# #         else:
# #             pdf.multi_cell(page_width, 8, line)

# #     pdf_bytes = pdf.output()  # Removed dest param (deprecated)
# #     return bytes(pdf_bytes)  # Convert bytearray to bytes
# def create_exam_pdf(textuc, subject, chapter):
#     text = clean_math_latex(textuc)
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_margins(15, 15, 15)
    
#     font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'DejaVuSans.ttf')
#     pdf.add_font('DejaVu', '', font_path)
#     pdf.add_font('DejaVu', 'B', font_path)
    
#     page_width = pdf.w - 2 * pdf.l_margin

#     # Title
#     pdf.set_font("DejaVu", 'B', 16)
#     header = f"Class 10 Model Paper - {subject} - {chapter}"
#     pdf.cell(0, 12, header, ln=True, align="C")
#     pdf.ln(10)

#     # Parse the text line by line for sections and questions
#     lines = text.split('\n')
#     for line in lines:
#         line = line.strip()
#         if not line:
#             pdf.ln(5)
#             continue

#         # Check if line is a section header (simple heuristic: starts with '**Section')
#         if line.startswith("**Section"):
#             # Clean the line from markdown asterisks
#             section_title = line.replace("**", "")
#             pdf.set_font("DejaVu", 'B', 14)
#             pdf.cell(0, 10, section_title, ln=True)
#             pdf.ln(3)
#         else:
#             # Regular question or text
#             pdf.set_font("DejaVu", '', 12)
#             pdf.multi_cell(page_width, 6, line)
#             pdf.ln(2)
    
#     pdf.ln(10)
#     pdf.set_font("DejaVu", 'I', 12)
#     pdf.cell(0, 10, "*End of Paper*", ln=True, align="C")

#     pdf_bytes = pdf.output(dest='S').encode('latin1')  # output as bytes string
#     return pdf_bytes

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         subject = request.form['subject']
#         chapter = request.form['chapter']
#         difficulty = request.form['difficulty']

#         paper_text = generate_paper(subject, chapter, difficulty)

#         pdf_content = create_exam_pdf(paper_text, subject, chapter)

#         response = Response(pdf_content, mimetype='application/pdf')
#         response.headers.set('Content-Disposition', 'attachment', filename=f"{subject}_{chapter}_model_paper.pdf")
#         response.headers['Content-Length'] = len(pdf_content)
#         return response

#     return render_template('form.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)

from flask import Flask, render_template, request, Response
import os
from openai import OpenAI
from fpdf import FPDF, XPos, YPos
import re

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("PERPLEXITY_API_KEY"),
    base_url="https://api.perplexity.ai"
)

# -------------------- Generate Paper --------------------
def generate_paper(subject, chapter, difficulty):
    prompt = (
        f"Create a model paper for class 10 {subject}, "
        f"{chapter} chapter, difficulty: {difficulty}. Structure as Section A (10x1), B (4x2), "
        "C (2x4), D (1x4), with suitable questions. Some extra requirement are ",f"{suggestions}" "Use plain text and clean mathematical symbols. "
        "Avoid LaTeX, avoid \\( \\), avoid $$. Use superscripts (x²), fractions (a/b), etc. Make questions strictly based difficulty level but add one difficult question in all levels.Follow the qustions format and syllabus of andhra pradesh board for all classes and formats.Give response as exam question paper no hint or extra descriptions in response of any kind, since response is being printed as pdf."
    )
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
# def sanitize_text(text):
#     replacements = {
#         '–': '-',  # en dash to hyphen
#         '—': '-',  # em dash to hyphen
#         '“': '"',
#         '”': '"',
#         '‘': "'",
#         '’': "'",
#         # Add other replacements if needed
#     }
#     for orig, repl in replacements.items():
#         text = text.replace(orig, repl)
#     return text


def create_exam_pdf(text, subject, chapter):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    # Load Unicode font
    font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'DejaVuSans.ttf')
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.add_font("DejaVu", "I", font_path, uni=True)

    page_width = pdf.w - 2 * pdf.l_margin

    # Header
    pdf.set_font("DejaVu", "B", 16)
    header = f"Class 10 Model Paper – {subject} – {chapter}"
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
            pdf.multi_cell(page_width, 6, line)
            pdf.ln(1)

    # Footer
    pdf.ln(5)
    pdf.set_font("DejaVu", "I", 12)
    pdf.cell(0, 10, "*End of Paper*", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    return pdf.output(dest="S").encode("latin1")  # PDF as bytes

# -------------------- Routes --------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        chapter = request.form['chapter']
        difficulty = request.form['difficulty']

        paper_text = generate_paper(subject, chapter, difficulty)
        pdf_content = create_exam_pdf(paper_text, subject, chapter)

        response = Response(pdf_content, mimetype='application/pdf')
        response.headers.set('Content-Disposition', 'attachment', filename=f"{subject}_{chapter}_model_paper.pdf")
        response.headers['Content-Length'] = len(pdf_content)
        return response

    return render_template('form.html')

# -------------------- Run --------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
