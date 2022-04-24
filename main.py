#!/usr/bin/env python3
import re
import argparse
import os
from datetime import datetime
import pandas as pd

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
time_format = "%H:%M"
parsed_text = ""

def fix_indent(t, indent_lvl, is_highlight):
    prefix = (">" if is_highlight else "")
    txt = indent_lvl*"\t" + "- "
    for line in t.split('\n'):
        txt += prefix + " " + line.strip() + "\n" # strip because of leading whitespace
        prefix = indent_lvl*'\t' +  ("  >" if is_highlight else "  ")
    return txt.rstrip("\n") #for loop leaves a trailing newline character.

def md_export(d):
    global parsed_text # to access the global variable parsed_text
    for book in d:
        parsed_text += "# {}\n".format(book)
        for page in d[book]:
            parsed_text += "- p{}\n".format(page)
            for note in d[book][page]: # this is a list: [date, quote, note] if note else [date, quote]
                parsed_text += "\t- On {}\n".format(note[0].strftime(date_format + " at " + time_format))
                parsed_text += fix_indent(note[1], 2, True)
                parsed_text += "\n"
                if len(note) > 2: # then there's a note
                    parsed_text += "\t\t\t- {}\n".format(note_prefix)
                    parsed_text += fix_indent(note[2], 4 ,False)
                    parsed_text += "\n"
        parsed_text += delim +"\n"
    return parsed_text

def write_to_file(t, output_file):
    with open(output_file, 'w+') as f:
        f.write(t)

def sanitize(unit):
    a = re.sub('^\n','', unit)
    b = re.sub('\n\s{2,}','\n', a) #For quotes. Removes leading white space in multi line highlights.
    c = re.sub('\n$','', b) #This is for notes since they always have trailing new line characters
    return c

def parse_text(blocks):
    d = {}
    for block in blocks:
        m = block_re.search(block) # m for match
        if m:
            if m.group("type") == "Lesezeichen":
                continue
            else:
                book = m.group("title")
                page = m.group("page")
                quote = sanitize(m.group("quote"))
                note = sanitize(m.group("note"))
                date_string = "{}.{}.{} at {}:{}".format(
                                                        m.group("year"),
                                                        m.group("month"),
                                                        m.group("day"),
                                                        m.group("hour"),
                                                        m.group("minute"))
                date = datetime.strptime(date_string, "%Y.%m.%d at %H:%M")
                if book in d.keys():
                    d[book]["page"].append(page)
                    d[book]["date"].append(date.date())
                    d[book]["time"].append(date.time())
                    d[book]["quote"].append(quote)
                    d[book]["note"].append(note if note else False)
                else:
                    d[book] = {"page": [page], "date": [date.date()], "time": [date.time()], "quote": [quote], "note": [note if note else False]}
    return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', type=str, required=False)
    ap.add_argument('-o', type=str, required=False)
    args = ap.parse_args()
    notes_file = os.path.abspath(args.i) if args.i else "notes.txt"
    output_file = os.path.abspath(args.o) if args.o else "output.txt"

    with open(notes_file) as f:
        text = f.read()

    blocks = text.split(delim)
    d = parse_text(blocks)
    for book in d:
        print("# {}".format(book))
        df = pd.DataFrame.from_dict(d[book])
        to_delete = df[df.duplicated(["quote"], keep="last")].index
        book_notes = df.drop(to_delete)
        print(book_notes.reset_index())
        print(delim)

    #print(md_export(d))
    #write_to_file(md_export(d), output_file)

if(__name__=="__main__"):
    main()
