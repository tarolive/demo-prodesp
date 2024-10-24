def process_document(file):

    from pypdf import PdfReader

    pdf_reader = PdfReader(file)
    pdf_pages  = pdf_reader.pages

    result = []

    for index, page in enumerate(pdf_pages):

        text     = process_text(page.extract_text())
        subjects = process_subjects(text)

        document = {
            'index'    : index,
            'text'     : text,
            'subjects' : subjects
        }

        result.append(document)

    return result


def process_text(text):

    from re import sub

    # names
    text = text.replace('EE RINALDO POLI PREFEITO', 'ESCOLA')
    text = text.replace('Faustin o', 'Faustino')
    text = text.replace('CASS IA', 'CASSIA')
    text = text.replace('ARTHUR LUIS PINHO DE LIMA', '')

    # locales
    text = text.replace('Região Miracatu', '')
    text = text.replace('Região Norte 1', '')
    text = text.replace('Região Taubaté', '')

    # patterns
    text = text.replace('EXONERA,', 'exonera,')
    text = text.replace('EXONERA ,', 'exonera,')
    text = text.replace('exonera ,', 'exonera,')
    text = text.replace('NOMEIA,', 'nomeia,')
    text = text.replace('NOMEIA ,', 'nomeia,')
    text = text.replace('nomeia ,', 'nomeia,')
    text = text.replace('AUTORIZA', 'autoriza,')
    text = text.replace('autoriza', 'autoriza,')
    text = text.replace('CESSA', 'cessa,')
    text = text.replace('cessa', 'cessa,')

    text = sub(r'exonera,[\s\S]*?(:)', 'exonera,', text)
    text = sub(r'nomeia,[\s\S]*?(:)', 'nomeia,', text)
    text = sub(r'vago em decorrência da exoneração de[\s\S]*?(\.)', '', text)
    text = sub(r'vago em decorrência da exoneração de[\s\S]*?(;)', '', text)
    text = sub(r'Diretor(.*)', '', text)
    text = sub(r'Assessor(.*)', '', text)

    # fields
    text = sub(r'(RG ([\d.\/-]?)*)', '', text)
    text = sub(r'(R.G. ([\d.\/-]?)*)', '', text)

    # clean
    text = text.replace('\xa0', '')
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')
    text = text.strip()

    return text


def process_subjects(text):

    subjects = []

    subjects += get_subjects(text, 'exonera,', 'exoneração')
    subjects += get_subjects(text, 'nomeia,', 'nomeação')

    return subjects


def get_subjects(text, pattern, type):

    from re import finditer

    subjects = []

    for index in [s.start() for s in finditer(pattern, text)]:

        subjects.append({
            'type'  : type,
            'index' : index
        })

    return subjects


def get_subject_text(text, text_index, index, size = 512):

    current_text = text[text_index]['text']
    subject_text = current_text[index : index + size]

    if len(subject_text) < size and text_index < len(text) - 1:

        next_text     = text[text_index + 1]['text']
        subject_text += ' ' + next_text[0 : size - len(subject_text) - 1]

    for remove in [
        'exonera,',
        'nomeia,',
        'autoriza,',
        'cessa,'
    ]:

        i = subject_text.find(remove, 1)
        if i > 0:
            subject_text = subject_text[0 : i]

    return subject_text
