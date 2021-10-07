#!/usr/bin/env python
"""
Prepare pages prepares all files in "files" for GitHub Pages

This script takes one argument, which specifies if the actions it should take are before the command
"git switch gh-pages" or afterwards. "before" means that it will the pre-change actions and "after" the after-change
actions.

This script processes files on how they are configured in the "files" dictionary: If the type is documentation
if will call pdoc3 to create the documentation for it. If the type is "page", the argument "convert_with_pandoc"
is a boolean which specifies, if the file should be converted into HTML by pandoc (True) or GitHub Pages' Jekyll
(False). If set to false, it is advised to set "convert_tables" to True, as Jekyll can not handle markdown tables.
Afterwards this script will replace all the links specified in the list "replace_links". There the first argument of
the Tuple specifies the old link and the second argument the new link. With "new_name" the file will be renamed on the
website.

Usage:
-----
- python3 prepare_pages.py before
  - Invokes actions before the branch switch
- python3 prepare_pages.py after
  - Invokes actions after the branch switch

Exit Codes:
----------
- 0: Everything is OK.
- 1: An internal error occurred
- 2: The user did not specify the right/enough arguments
"""
import os
from os.path import exists
import sys
from urllib import request


"""
The files dictionary specifies how and which files should be processed.

Structure:
---------
- Filename or directory (directory only with type=documentation)
  - type:
    - page: Converts into static webpage
    - documentation: calls pdoc3 to create a documentation for it
  - replace_tables: Boolean: If tables should be replaced by HTML-Tables
  - replace_links: A list of tuples for links th be replaced in this document
    - element one: The link that should be replaced
    - element two: The link that element one should be replaced with
  - convert_with_pandoc: boolean: If the page should be converted with pandoc (True) or Jekyll (False)
  - new_name: the new filename and the name on the website. If convert_with_pandoc is set to true,
    make the extension .html. If the name should not be changed, put in None.
"""
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
    """Replaces all markdown tables in _text with html tables

    This function writes the mardkwon table to a temporary file in /tmp/, calls pandoc to convert this file to html and
    reads the text back in.

    Arguments:
    ---------
    - _text: The text in which all the tables should be converted.

    Returns:
    -------
    The input string, but with repkaced markdown tables.
    """
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


def get_header(url: str = r'https://lxgr-linux.github.io/pokete',
                header_end: str = r'<section>') -> str:
    """Gets the first part of a webpage

    Arguments:
    ---------
    - url: The URL to get the first part of.
    - header_end: the end of the "header".

    Returns:
    -------
    The start of this webpage.
    """
    result = request.urlopen(url)
    _text = result.read().decode('UTF-8').split(header_end)[0]
    return _text + header_end + '\n'


def get_footer(url: str = r'https://lxgr-linux.github.io/pokete',
        footer_start: str = r'</section>') -> str:
    """Gets the last part of a webpage

    Arguments:
    ---------
    - url: The URL to get the last part of.
    - footer_start: Where the "footer"/the end of the webpage begins.

    Returns:
    -------
    The end of this webpage.
    """
    result = request.urlopen(url)
    _text = result.read().decode('UTF-8').split(footer_start)[1]
    _text = footer_start + _text
    return _text


def create_documentation() -> None:
    """Creates documentation for all tagged files

    This function creates python documentation for all files and folders in the files dictionary that have the type
    "documentation". This function will call pandoc to create the documentation for it.
    """
    modules = [file for file in files if files[file]["type"] == "documentation"]
    pdoc_path = "/home/runner/.local/bin/pdoc"

    for module in modules:
        print(f"==> {module}")
        os.system(f"{pdoc_path} --html {module} --output-dir \"/tmp/doc/\" --force")


def before() -> None:
    """The actions taht should be executed before the brach switch

    This functions creates documentation for all the files, replaces tables if necessary or converts the files with
    pandoc. All the files are then moved into the /mp directory.
    """
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
    """The actions that shall be executed in the gh-pages branch.

    This function copies akk oreviously created files from /tmo/ to the current working directry and adds the start
    and end of the gh-pages index website to the files which have been converted with pandoc. This achieves a universal
    look on all gh-pages pages. This function then replaces all the links for each file.
    """
    print(':: After processing files for gh-pages...')
    print(':: Acquiring assets...')
    print('==> header')
    header = get_header(url='https://lxgr-linux.github.io/pokete', header_end='<section>')
    print(header)
    print('==> footer')
    footer = get_footer(url='https://lxgr-linux.github.io/pokete', footer_start='</section>')
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
