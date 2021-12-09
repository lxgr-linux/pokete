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
import json
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
files = {}


def replace_tables(_text: str) -> str:
    """Replaces all markdown tables in _text with html tables

    This function writes the mardkwon table to a temporary file in /tmp/, calls pandoc to convert this file to html and
    reads the text back in.

    Arguments:
    ---------
    - _text: The text in which all the tables should be converted.

    Returns:
    -------
    The input string, but with replaced markdown tables.
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
    "documentation". This function will call pdoc to create the documentation for it.
    """
    modules = [file for file in files if files[file]["type"] == "documentation"]
    pdoc_path = "/home/runner/.local/bin/pdoc"

    for module in modules:
        print(f" -> {module}")
        os.system(f"{pdoc_path} --html {module} --output-dir \"/tmp/doc/\" --force")


def add_folder(folder: str, add_tmp_folder: bool = False) -> None:
    """Creates a folder, if not does not already exist

    This function creates a folder in the current working directory.
    It also creates a folder with the same name in /tmp, if needed.

    Arguments
    ---------
    folder: The name of the folder to create
    add_tmp_folder If a folder in /tmp should be creates as well.
    """
    if not os.path.isdir(folder):
        os.mkdir(folder)
    tmp_folder = os.path.join("/tmp", folder)
    if not os.path.isdir(tmp_folder):
        os.mkdir(tmp_folder)
    files.update({
        folder: {
            "type": "folder"
        }
    })


def create_wiki() -> None:
    """Creates a multi-page and a single-page wiki.

    This function calls the multi-page and single-page methods from the
    gen_wiki file to add to the gh-pages.
    """
    from gen_wiki import Wiki
    Wiki.multi("./wiki-multi-md/")
    Wiki.single("./wiki-single.md")


def add_wiki_folder(folder_name: str) -> list:
    """Gives out all markdown files in current and subdirectories as a list

    This function adds all markdown files in the current directory to the list
    is gives back. It also calls itself for each sub-directory and appends the
    markdown files from itself to the output list as well.

    Arguments
    ---------
    folder_name: The folder to add

    Returns:
    --------
    A list of all markdown files in the current and all subdirectories.
    """
    items = os.listdir(folder_name)
    out = []
    for item in items:
        file = os.path.join(folder_name, item)
        if os.path.isdir(file):
            add_folder(file.replace("./wiki-multi-md/", "./wiki-multi-html/"), True)
            for f in add_wiki_folder(file):
                out.append(f)
        elif os.path.isfile(file):
            if item.endswith(".md"):
                out.append(file)
            else:
                print(f"{file} is not a markdown file!")
        else:
            print(f"Unrecognized type: {file}")
    return out


def add_wiki_to_files() -> None:
    """Add files from multi-page wiki to files dictionary

    This function adds all markdown files from the directory ./wiki-multi-md
    and its subdirectories into the files dictionary to be processed by the other functions as well.
    """
    if not os.path.isdir("./wiki-multi-html"):
        os.mkdir("./wiki-multi-html")
    if not os.path.isdir("/tmp/wiki-multi-html"):
        os.mkdir("/tmp/wiki-multi-html")
    wiki_files = add_wiki_folder("./wiki-multi-md/")
    print(wiki_files)
    for wiki_file in wiki_files:
        files.update({
                wiki_file: {
                    "type": "page",
                    "replace_tables": False,
                    "convert_with_pandoc": True,
                    "replace_links": [],
                    "new_name": str(wiki_file.replace(".md", ".html")).replace("./wiki-multi-md/", "./wiki-multi-html/")
                }
            })
    print(files)


def before() -> None:
    """The actions that should be executed before the brach switch

    This functions creates documentation for all the files, replaces tables if necessary or converts the files with
    pandoc. All the files are then moved into the /mp directory.
    """
    print(':: Preparing files for gh-pages...')
    print("==> Generating documentation with pdoc...")
    create_documentation()
    print("==> Creating Wiki...")
    create_wiki()
    print("==> Adding Multi-page Wiki...")
    add_wiki_to_files()
    for file in files.keys():
        print(f"==> Preparing {file}")
        properties = files[file]

        if properties["type"] == "documentation" or properties["type"] == "folder":
            continue

        new_name = properties["new_name"] if properties["new_name"] is not None else file

        # Jekyll can not handle double open/closing brackets (e.g. {{) , so we
        # need to manually convert these pages.
        # We do this by using pandoc and adding the start and end of the
        # root page to the start and the end of the
        if properties["convert_with_pandoc"]:
            print(" -> Converting to html...")
            os.system(f"pandoc --from gfm --to html5 -o \"{new_name}\" \"{file}\"")

        # Tables only need to be replaced, if the file is not converted with
        # pandoc, as pandoc is converting the tables automatically.
        elif properties["replace_tables"]:
            print(" -> Replacing Tables...")
            with open(file, 'r') as f:
                text = f.read()
                text = replace_tables(text)
            with open(new_name, 'w') as f:
                f.write(text)

        # If no operation was performed, we need to move the file, in order to
        # not interrupt the workflow.
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

    This function copies all previously created files from /tmp/ to the current
    working directory and adds the start and end of the gh-pages index website
    to the files which have been converted with pandoc. This achieves a universal
    look on all gh-pages pages. This function then replaces all the links for
    each file.
    """
    print(':: After processing files for gh-pages...')
    print(':: Acquiring assets...')
    print('==> header')
    header = get_header(url='https://lxgr-linux.github.io/pokete',
                        header_end='<section>')
    print(header)
    print('==> footer')
    footer = get_footer(url='https://lxgr-linux.github.io/pokete',
                        footer_start='</section>')
    print(footer)
    # We need to store the configuration to keep the "new_name" attribute from
    # the before run.
    print(":: Loading configuration...")
    with open('/tmp/prepare_pages_saves.py', 'r') as f:
        text = f.read()
        new_files = eval(text)

    print(':: Processing files...')
    print('==> Making directories...')
    print(' -> wiki-multi-html')
    add_folder('wiki-multi-html', False)
    for file in new_files.keys():
        properties = new_files[file]
        if properties["type"] == "folder":
            print(' -> ' + file)
            add_folder(file, False)
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
        elif properties["type"] == "folder":
            continue

        new_name = properties["new_name"] if properties["new_name"] is not None else file
        print(f'==> After processing {new_name}')

        # If a file was converted with pandoc, it needs the stylesheet
        # (in the header) and a footer.
        if properties["convert_with_pandoc"]:
            print("-> Applying Styles...")
            with open(f"/tmp/{new_name}", 'r') as f:
                text = f.read()
            with open(new_name, 'w') as f:
                f.write(header + text + footer)
        else:
            print(" -> Copying to current directory...")
            os.system(f"cp \"/tmp/{new_name}\" .")

        # Links need to be replaced from directory and markdown direct links
        # (wiki.md) into website links (./wiki)
        if properties["replace_links"]:
            print(" -> Replacing links...")
            for old in properties["replace_links"].keys():
                new = properties["replace_links"][old]
                if old != list(properties["replace_links"].keys())[-1]:
                    print(f" |-> Replacing {old} with {new}...")
                else:
                    print(f" `-> Replacing {old} with {new}...")
                # Need to use sed, as str.replace somehow misses some link
                # changes?
                os.system(f"sed -i 's#]({old}#]({new}#g' {new_name}")
    print("==> Renaming 'wiki-multi-html' to 'wiki-multi'...")
    os.system("mv './wiki-multi-html/' './wiki-multi'")
    print(':: Done!')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Error! Not enough arguments:')
        print(f"Usage: '{sys.argv[0]}' <after|before>")
        sys.exit(2)
    if sys.argv[1] == 'before':
        with open('.gh-pages.json', 'r') as config_file:
            files = json.loads(config_file.read())
        before()
    elif 'after' == sys.argv[1]:
        after()
    else:
        print('Error! Unrecognised first argument:')
        print(f"Usage: '{sys.argv[0]}' <after|before>")
        sys.exit(2)
