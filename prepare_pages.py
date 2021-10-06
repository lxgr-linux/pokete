#!/usr/bin/env python
import os
import sys
from urllib import request

if __name__ != '__main__':
    sys.exit(1)


def replace_tables(_text: str) -> str:
    out = ''
    table = ''
    in_table = False
    for line in _text.split('\n'):
        if '|' in line:
            in_table = True
            table += line
            table += '\n'
            #print(line)
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


if __name__ == '__main':
    if len(sys.argv) == 1:
        print('Error! Not enough arguments:')
        print(f"Usage: '{sys.argv[0]}' <after|before>")
        sys.exit(2)
    if sys.argv[1] == 'before':
        print(':: Preparing files for gh-pages...')
        for file in ['README.md', 'Changelog.md', 'HowToPlay.md']:
            print(f"==> Preparing {file}")
            with open(file, 'r') as f:
                text = f.read()
                text = replace_tables(text)
            with open(file, 'w') as f:
                f.write(text)
        print(':: Done!')
    elif 'after' == sys.argv[1]:
        print(':: After processing files for gh-pages...')
        print(':: Acquiring assets...')
        print('==> header')
        header = get_header('https://lxgr-linux.github.io/pokete')
        print(header)
        print('==> footer')
        footer = get_footer('https://lxgr-linux.github.io/pokete')
        print(footer)
        print('Precessing files...')
        for file in ['wiki.html']:
            print(f'==> {file}')
            with open(file, 'r') as f:
                text = f.read()
            with open(file, 'w') as f:
                f.write(header + text + footer)
        print(':: Done!')
    else:
        print('Error! Unrecognised first argument:')
        print(f"Usage: '{sys.argv[0]}' <after|before>")
        sys.exit(2)

