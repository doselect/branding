from __future__ import print_function
import json
import os
import sys
import subprocess

CONFIG_FILE_PATH = 'config.json'

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            return json.load(f)
    except:
        print("ERROR: %s not found!" % CONFIG_FILE_PATH, file=sys.stderr)

def has_inkscape():
    return any([os.path.exists(p) for p in [os.path.join(p, 'inkscape') for p in os.environ['PATH'].split(':')]])

def export_image(file_name, height, width, export_ext, export_dir):
    export_file_name = "%s_%dx%d.%s" % (os.path.splitext(file_name)[0], height, width, export_ext)
    export_full_path = os.path.join(export_dir, export_file_name)
    p = subprocess.call([
            'inkscape',
            '-f', file_name,
            '-h', str(height),
            '-w', str(width),
            '-e', export_full_path
        ])

def main():

    if not has_inkscape():
        print("ERROR: Inkscape not found!", file=sys.stderr)
        return
    
    config = load_config()

    if not os.path.exists(config['export_directory']):
        os.makedirs(config['export_directory'])

    for image in config['files']:

        print("INFO: Exporting %d images for %s" % (len(image['sizes']), image['name']))

        for size in image['sizes']:

            export_image(image['name'], size[0], size[1], image['export_ext'], config['export_directory'])

        print("INFO: Done!")

if __name__ == "__main__":
    main()
