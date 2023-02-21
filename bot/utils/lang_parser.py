import yaml


def get_phrase(phrase_type: str, *args) -> str:
    try:
        with open('/bot/bot_phrases.yml', 'r') as f:
            phrases_file = yaml.safe_load(f)
            phrase = phrases_file[phrase_type]
    except FileNotFoundError:
        return 'Бот забыл слова'

    if args:
        args = list(args)
        while '{}' in phrase:
            phrase = phrase.replace('{}', args.pop(0), 1)

    return phrase
