#!/usr/bin/env python
import re
import os
import jinja2

CMDLETS_FILE = "./cmdlets.txt"
ACTION_TEMPLATE_PATH = "./action_template.yaml"


def convert(name):
    s0 = name.replace('-', '')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s0)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def render_action(context):
    path, filename = os.path.split(ACTION_TEMPLATE_PATH)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def read_file_lines(filename):
    with open(CMDLETS_FILE) as f:
        content = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]
    return content

def main():
    cmdlet_lines = read_file_lines(CMDLETS_FILE)
    context = {}
    context['cmdlet_camel_case'] = None
    context['cmdlet_snake_case'] = None
    context['description'] = None

    # File format
    #  Cmdlet-CamelCase
    #  Cmdlet description string
    #  Cmdlet2-CamelCase
    #  Cmdlet2 description string
    #  ...
    for idx, line in enumerate(cmdlet_lines):
        if (idx % 2 == 0): # is even
            context['cmdlet_camel_case'] = line
            context['cmdlet_snake_case'] = convert(line)
        else: # is even
            context['description'] = line
            action_data = render_action(context)
            action_filename = "../actions/{}.yaml".format(context['cmdlet_snake_case'])
            with open(action_filename, "w") as f:
                f.write(action_data)

if __name__ == "__main__":
    main()
