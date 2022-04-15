import re
import argparse
import os

#delimetor between not blocks
delim = "-----------------------------------"

#regex for a note block
block_re = re.compile(r'\n'.join([
    r'(?P<title>.+)',
    r'((?P<type>Lesezeichen|Markierung|Notiz)\sauf\sSeite\s(?P<page>\d+):\s)' + r'''((?P<note>(?:.|\n)*))?''' + r'"(?P<quote>(?:.|\n)*)"',
    r'(Hinzugefügt|Geändert)\sam\s(?P<day>\d{2}).(?P<month>\d{2}).(?P<year>\d{4})',
    ]))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', type=str, required=False)
    args = ap.parse_args()
    notes_file = os.path.abspath(args.i) if args.i else "notes.txt"
    with open(notes_file) as f:
        text = f.read()
        #text = text.replace(u'\xa0', u' ')
        #text = re.sub('^\s*',"", text)
    blocks = text.split(delim)
    for block in blocks:
        m = block_re.search(block)
        if m:
            print(m.group("title"))
            print(m.group("quote"))
            if m.group("note"):
                print(m.group("note"))
            print(delim)

if(__name__=="__main__"):
    main()
