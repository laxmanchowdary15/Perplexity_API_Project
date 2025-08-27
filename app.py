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
        model="sonar-reasoning-pro",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_exam_pdf(text, subject, chapter):
    from fpdf import FPDF
    import os

    pdf = FPDF()
    pdf.add_page()

    # Set margins and font
    pdf.set_margins(10, 10, 10)
    font_path = os.path.join(os.path.dirname(__file__), 'static', 'fonts', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font("DejaVu", size=12)

    # Calculate printable width
    page_width = pdf.w - 2 * pdf.l_margin

    # Header
    header = f"Class 10 Model Paper - {subject} - {chapter}"
    pdf.cell(0, 10, header, ln=1, align="C")
    pdf.ln(5)

    # Add content line by line
    for line in text.split('\n'):
        if line.strip() == "":
            pdf.ln(5)
        else:
            pdf.multi_cell(page_width, 8, line)

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
