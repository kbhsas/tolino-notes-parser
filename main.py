#!/usr/bin/env python3
import re
import argparse
import os
from datetime import datetime

#delimetor between not blocks
delim = "-----------------------------------"

#regex for a note block
block_re = re.compile(r'\n'.join([
    r'(?P<title>.+)',
    r'((?P<type>Lesezeichen|Markierung|Notiz)\sauf\sSeite\s(?P<page>\d+):\s)' + r'''((?P<note>(?:.|\n)*))?''' + r'"(?P<quote>(?:.|\n)*)"',
    r'(Hinzugefügt|Geändert)\sam\s(?P<day>\d{2}).(?P<month>\d{2}).(?P<year>\d{4}) \| (?P<hour>\d{1,2}):(?P<minute>\d{2})',
    ]))
note_prefix = "[[literature notes]]"
date_format = "[[%Y.%m.%d %A]]"
parsed_text = ""

def md_export(d):
    global parsed_text # to access the global variable parsed_text
    for book in d:
        parsed_text += "# {}\n".format(book)
        for page in d[book]:
            parsed_text+= "- p{}\n".format(page)
            for note in d[book][page]: # this is a list: [date, quote, note] if note else [date, quote]
                parsed_text+= "\t- On {}\n".format(note[0].strftime(date_format + " at %H:%M"))
                parsed_text+= "\t\t- > {}\n".format(note[1])
                if len(note) > 2: # then there's a note
                    parsed_text+= "\t\t\t- {}\n".format(note_prefix)
                    parsed_text+= "\t\t\t\t- {}\n".format(note[2])
        parsed_text += delim +"\n"
    return parsed_text

def write_to_file(t):
    with open("output.txt", 'w+') as f:
        f.write(t)

def sanitize(unit):
    a = re.sub('^\n','', unit)
    b = re.sub('\s{2,}',' ', a) # This also removed newline characters from the middle of the string. It is a rare case but the LotR highlight in the dataset has it.
    return b

def main():
    d = {}
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', type=str, required=False)
    args = ap.parse_args()
    notes_file = os.path.abspath(args.i) if args.i else "notes.txt"
    with open(notes_file) as f:
        text = f.read()
    blocks = text.split(delim)
    for block in blocks:
        m = block_re.search(block) # m for match
        if m:
            book = m.group("title")
            page = m.group("page")
            quote = sanitize(m.group("quote"))
            note = m.group("note")
            date_string = "{}.{}.{} at {}:{}".format(
                                                    m.group("year"),
                                                    m.group("month"),
                                                    m.group("day"),
                                                    m.group("hour"),
                                                    m.group("minute"))
            date = datetime.strptime(date_string, "%Y.%m.%d at %H:%M")
            if book in d.keys():
                if page in d[book]:
                    d[book][page].append([date, quote, note] if note else [date, quote])
                else:
                    d[book][page] = [[date, quote, note]] if note else [[date, quote]]
            else:
                d[book] = {page: [[date, quote, note]]} if note else {page: [[date, quote]]}
    print(md_export(d))
    #write_to_file(md_export(d))

if(__name__=="__main__"):
    main()
