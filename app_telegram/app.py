from components.nlp              import nlp
from components.process_document import get_subject_text, process_document
from flask                       import Flask, request
from json                        import dumps
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

    # handle text request

    request_text = message['request']['text']

    if request_text is not None:

        # /start

        if request_text.startswith('/start'):

            first_name    = message['request']['from']['first_name']
            response_text = f'Olá { first_name }! Poderia me enviar um diário oficial para análise?'

        else:
            response_text = 'Sou assistente que realiza análise de diários oficiais da PRODESP.'

        # send text response

        params = {
            'chat_id' : message['request']['chat']['id'],
            'text'    : response_text
        }

        api = f'{ TELEGRAM_API }/sendMessage'
        get(url = api, params = params)

        # update response

        message['response']['text'] = response_text

    print(dumps(message, indent = 4))
    return message
