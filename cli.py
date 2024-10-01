import click
from simpleGUI import SimpleGUI

@click.command()
@click.option('--image_file', help='Input image.')

def runApp(image_file):
    click.echo(f"Image file: {image_file}")
    app = SimpleGUI(image_file)
    app.start()

if __name__ == '__main__':
    runApp()
