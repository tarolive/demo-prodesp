from components.process_document import process_document
from flask                       import Flask, request

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def process_document() -> dict:

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

    text = process_document(file.filename)

    return text
