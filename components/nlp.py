def nlp(text):

    from torch        import argmax
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    model_name = 'pierreguillou/ner-bert-base-cased-pt-lenerbr'

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model     = AutoModelForTokenClassification.from_pretrained(model_name)

    encoding    = tokenizer(text, max_length = 512, truncation = True, return_tensors = 'pt')
    predictions = argmax(model(**encoding).logits, dim = 2)[0].numpy()

    entities = get_entities(text, model, encoding, predictions)

    return entities


def get_entities(text, model, encoding, predictions):

    entities = {
        'pessoas' : []
    }

    start = None
    type  = None

    for index, prediction in enumerate(predictions):

        prediction = model.config.id2label[prediction]

        if not type and prediction == 'B-PESSOA':

            start = index
            type  = 'pessoas'

            continue

        if type and prediction == 'O':

            start, _ = encoding.token_to_chars(start)
            _, end   = encoding.token_to_chars(index - 1)

            entity = text[start : end]
            entities[type].append(entity)

            start = None
            type  = None

    return entities
