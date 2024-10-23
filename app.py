from components.nlp              import nlp
from components.process_document import get_subject_text, process_document
from flask                       import Flask, request

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def app() -> list:

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

    result = {
        'exoneração' : [],
        'nomeação'   : []
    }

    for subject in subjects:

        if subject['type'] == 'exoneração':

            result['exoneração'] += subject['pessoas']

        else:

            result['nomeração'] += subject['pessoas']

    result['exoneração'] = list(set(result['exoneração']))
    result['nomeação'] = list(set(result['nomeação']))

    return result
