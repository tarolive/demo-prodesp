from components.nlp              import nlp
from components.process_document import get_subject_text, process_document
from flask                       import Flask, request

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def process_document() -> list:

    if 'file' not in request.files:
        return {
            'error' : 'File not found'
        }

    file = request.files['file']

    if file.filename == '':
        return {
            'error' : 'File not selected'
        }

    file.save(file.filename)

    text     = process_document(file.filename)
    subjects = []

    for page in text:

        for subject in page['subjects']:

            subject_text   = get_subject_text(text, page['index'], subject['index'])
            subject['nlp'] = nlp(subject_text)

            subjects.append(subject)

    return subjects
