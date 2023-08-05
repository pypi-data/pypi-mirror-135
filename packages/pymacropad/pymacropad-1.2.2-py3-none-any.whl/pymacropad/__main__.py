import click

from .macropad import start

@click.command()
def main():
    start()

if __name__ == '__main__':
    main()
