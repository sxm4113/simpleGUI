import click
import os
import sys
from exceptions import ImageNotFound, ModelParameterNotFound

@click.command()
@click.option("--image_file", help='Input for Contrast Enahnacement')
@click.option("--image_folder", help='Input folder for Classification')
@click.option("--parameter_file", help='.pt file for Classification model')

def cli(image_file, image_folder, parameter_file):
 
    try:
        if not (os.path.exists(image_file)):
            raise ImageNotFound ("Error-Image not found")
        elif not (os.path.exists(image_folder)):
            raise ImageNotFound ("Error-Image not found")
        elif not (os.path.exists(parameter_file)):
            raise ModelParameterNotFound ("Error-Parameter File not found")
    except (ImageNotFound, ModelParameterNotFound) as e:
        print (e)
        sys.exit(1)

    input_info = {'image_file':image_file,
                    'image_folder':image_folder,
                    'parameter_file':parameter_file}

    print ("input_info: ", input_info)
    # app = SimpleGUI(input_info)
    # app.start()

if __name__ == '__main__':
    cli()
