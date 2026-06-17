import PyPDF2
import docx

# PDF READER

def extract_text_pdf(file):

    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text

# DOCX READER

def extract_text_docx(file):

    doc = docx.Document(file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text
