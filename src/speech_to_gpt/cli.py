import click

from speech_to_gpt.api_calls import login, main as converse
@click.group()
def main():
    pass

@main.command()
@click.option(
    '--api-key',
    required=True,
    help="Your OpenAI API key."
)
def config(api_key):
    login(api_key)

@main.command()
@click.option(
    '--lang',
    '-language',
    default='English',
    help='Language to converse in.'
)
def chat(lang):
    converse(language=lang)

if __name__ == '__main__':
    main()