from components.nlp              import nlp
from components.process_document import get_subject_text, process_document
from flask                       import Flask, request
from json                        import dumps, loads
from os                          import getenv
from os.path                     import join
from requests                    import get

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
TELEGRAM_API   = f'https://api.telegram.org/bot{ TELEGRAM_TOKEN }'

app = Flask(__name__)


@app.route('/', methods = ['POST'])
def telegram() -> dict:

    # create response

    message = {
        'request'  : request.json,
        'response' : {}
    }

    # handle request

    request_text     = message['request']['text']
    request_document = message['request']['document']
    request_file_id  = None if request_document is None else request_document['file_id']

    if request_text is not None and request_file_id is None:

        # /start

        first_name    = message['request']['from']['first_name']
        response_text = f'Olá { first_name }! Sou assistente que realiza análise de diários oficiais da PRODESP.'

        # send text response

        params = {
            'chat_id' : message['request']['chat']['id'],
            'text'    : response_text
        }

        api = f'{ TELEGRAM_API }/sendMessage'
        get(url = api, params = params)

        # update response

        message['response']['text'] = response_text

    if request_file_id is not None:

        params = {
            'file_id' : request_file_id
        }

        api       = f'{ TELEGRAM_API }/getFile'
        file_path = loads(get(url = api, params = params).text)['result']['file_path']

        api  = f'https://api.telegram.org/file/bot{ TELEGRAM_TOKEN }/{ file_path }'
        file = get(url = api, params = params)

        filename = join('uploads', 'file.pdf')
        open(filename, 'wb').write(file.content)

        text     = process_document(filename)
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

                result['exoneração'] += subject['nlp']['pessoas']

            else:

                result['nomeação'] += subject['nlp']['pessoas']

        result['exoneração'] = list(set(result['exoneração']))
        result['nomeação'] = list(set(result['nomeação']))

        # send text response

        response_text = 'Segue análise do diário oficial enviado.\n\nExonerados:\n'

        if len(result['exoneração']) == 0:
            response_text += 'Não foram encontradas pessoas exoneradas.\n'
        else:
            for p in result['exoneração']:
                response_text += p + '\n'

        response_text += '\nNomeadas:\n'

        if len(result['nomeação']) == 0:
            response_text += 'Não foram encontradas pessoas nomeadas.\n'
        else:
            for p in result['nomeação']:
                response_text += p + '\n'

        params = {
            'chat_id' : message['request']['chat']['id'],
            'text'    : response_text
        }

        api = f'{ TELEGRAM_API }/sendMessage'
        get(url = api, params = params)

    print(dumps(message, indent = 4))
    return message
