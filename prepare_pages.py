#!/usr/bin/env python
import os
from os.path import exists
import sys
from urllib import request

files = {
    "README.md": {
        "type": "page",
        "replace_tables": True,
        "replace_links": [
            ("wiki.md", "./wiki"),
            ("Changelog.md", "./Changelog"),
            ("HowToPlay.md", "./HowToPlay")],
        "convert_with_pandoc": False,
        "new_name": "index.md"
    },
    "Changelog.md": {
        "type": "page",
        "replace_tables": True,
        "replace_links": [],
        "convert_with_pandoc": False,
        "new_name": None
    },
    "HowToPlay.md": {
        "type": "page",
        "replace_tables": True,
        "replace_links": [],
        "convert_with_pandoc": False,
        "new_name": None
    },
    "wiki.md": {
        "type": "page",
        "replace_tables": False,
        "replace_links": [],
        "convert_with_pandoc": True,
        "new_name": "wiki.html"
    },
    "gen-wiki.py": {
        "type": "documentation"
    },
    "pokete.py": {
        "type": "documentation"
    },
    "prepare_pages.py": {
        "type": "documentation"
    },
    "pokete_classes/": {
        "type": "documentation"
    },
    "pokete_data/": {
        "type": "documentation"
    }
}


def replace_tables(_text: str) -> str:
    out = ''
    table = ''
    in_table = False
    for line in _text.split('\n'):
        if '|' in line:
            in_table = True
            table += line
            table += '\n'
        else:
            if in_table:
                in_table = False
                with open('/tmp/pandoc_convert.md', 'w') as _f:
                    _f.write(table)
                os.system('pandoc /tmp/pandoc_convert.md -o /tmp/pandoc_convert.html')
                with open('/tmp/pandoc_convert.html', 'r') as _f:
                    md_text = _f.read()
                table = ''
                out += md_text
                out += '\n'
            else:
                out += line
                out += '\n'
    return out


def get_header(url):
    header_end = r'<section>'
    result = request.urlopen(url)
    _text = result.read().decode('UTF-8').split(header_end)[0]
    return _text + header_end + '\n'


def get_footer(url):
    footer_start = '</section>'
    result = request.urlopen(url)
    _text = result.read().decode('UTF-8').split(footer_start)[1]
    _text = footer_start + _text
    return _text


def create_documentation():
    modules = [file for file in files if files[file]["type"] == "documentation"]
    pdoc_path = "/home/runner/.local/bin/pdoc"

    for module in modules:
        print(f"==> {module}")
        os.system(f"{pdoc_path} --html {module} --output-dir \"/tmp/doc/\" --force")


def before() -> None:
    print(':: Preparing files for gh-pages...')
    print(":: Generating documentation with pdoc...")
    create_documentation()
    for file in files.keys():
        print(f"==> Preparing {file}")
        properties = files[file]

        if properties["type"] == "documentation":
            continue

        new_name = properties["new_name"] if properties["new_name"] is not None else file

        # Jekyll can not handle double open/closing brackets (e.g. {{) , so we need to manually convert these pages.
        # We do this by using pandoc and adding the start and end of the root page to the start
        # and the end of the
        if properties["convert_with_pandoc"]:
            print(" -> Converting to html...")
            os.system(f"pandoc --from gfm --to html5 -o \"{new_name}\" \"{file}\"")

        # Tables only need to be replaced, if the file is not converted with pandoc, as pandoc is converting the tables
        # automatically.
        elif properties["replace_tables"]:
            print(" -> Replacing Tables...")
            with open(file, 'r') as f:
                text = f.read()
                text = replace_tables(text)
            with open(new_name, 'w') as f:
                f.write(text)

        # If no operation was performed, we need to move the file, in order to not interrupt the workflow.
        else:
            os.system(f"mv \"{file}\" \"{new_name}\"")

        print(" -> Copying to /tmp...")
        os.system(f"cp \"{new_name}\" \"/tmp/{new_name}\"")

        files[file]["new_name"] = new_name

    print("Saving configuration...")
    with open('/tmp/prepare_pages_saves.py', 'w') as f:
        f.write(str(files))

    print(':: Done!')


def after() -> None:
    print(':: After processing files for gh-pages...')
    print(':: Acquiring assets...')
    print('==> header')
    header = get_header('https://lxgr-linux.github.io/pokete')
    print(header)
    print('==> footer')
    footer = get_footer('https://lxgr-linux.github.io/pokete')
    print(footer)
    # We need to store the configuration to keep the "new_name" attribute from the before run.
    print(":: Loading configuration...")
    with open('/tmp/prepare_pages_saves.py', 'r') as f:
        text = f.read()
        new_files = eval(text)

    print(':: Processing files...')
    documentation_copied = False
    for file in new_files.keys():
        properties = new_files[file]

        # Copy documentation folder from /tmp/doc/ to current directory
        if properties["type"] == "documentation":
            if not documentation_copied:
                print("==> Copying Documentation folder...")
                if exists("./doc/"):
                    print(" -> Removing old documentation folder...")
                    os.system(f"rm -rf doc")
                print(" -> Copying new documentation files...")
                os.system("cp -r /tmp/doc/ .")
                documentation_copied = True  # Only copy the directory once
            continue

        new_name = properties["new_name"] if properties["new_name"] is not None else file
        print(f'==> After processing {new_name}')

        # If a file was converted with pandoc, it needs the stylesheet (in the header) and a footer.
        if properties["convert_with_pandoc"]:
            print("-> Applying Styles...")
            with open(f"/tmp/{new_name}", 'r') as f:
                text = f.read()
            with open(new_name, 'w') as f:
                f.write(header + text + footer)
        else:
            print(" -> Copying to current directory...")
            os.system(f"cp \"/tmp/{new_name}\" .")

        # Links need to be replaced from directory and markdown direct links (wiki.md) into website links (./wiki)
        if properties["replace_links"]:
            print(" -> Replacing links...")
            with open(new_name, 'r') as f:
                text = f.read()
            for link in properties["replace_links"]:
                old, new = link
                if link != properties["replace_links"][-1]:
                    print(f" |-> Replacing {old} with {new}...")
                else:
                    print(f" `-> Replacing {old} with {new}...")
                old = f"]({old}"
                new = f"]({new}"
                text.replace(old, new)
            with open(new_name, 'w') as f:
                f.write(text)

    print(':: Done!')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Error! Not enough arguments:')
        print(f"Usage: '{sys.argv[0]}' <after|before>")
        sys.exit(2)
    if sys.argv[1] == 'before':
        before()
    elif 'after' == sys.argv[1]:
        after()
    else:
        print('Error! Unrecognised first argument:')
        print(f"Usage: '{sys.argv[0]}' <after|before>")
        sys.exit(2)
