#!/usr/bin/env python
import os
import sys

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


print(':: Preparing files for gh-pages...')
for file in ['README.md', 'Changelog.md', 'HowToPlay.md']:
    print(f"==> Preparing {file}")
    with open(file, 'r') as f:
        text = f.read()
        text = replace_tables(text)
    with open(file, 'w') as f:
        f.write(text)
print(':: Done!')

