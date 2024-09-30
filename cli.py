import click
from gui import SimpleGUIApp

@click.command()
@click.option('--image_file', help='Input image.')

def runApp(image_file):
    click.echo(f"Image file: {image_file}")
    SimpleGUIApp(image_file).run()

if __name__ == '__main__':
    runApp()
