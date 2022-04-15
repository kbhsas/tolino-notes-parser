import re

#delimetor between not blocks
delim = "-----------------------------------"

#regex for a note block
block_re = re.compile(r'\n'.join([
    r'(?P<title>.+)',
    r'((?P<type>Lesezeichen|Markierung|Notiz)\sauf\sSeite\s(?P<page>\d+):\s)' + r'''((?P<note>(?:.|\n)*))?''' + r'"(?P<quote>(?:.|\n)*)"',
    r'(Hinzugefügt|Geändert)\sam\s(?P<day>\d{2}).(?P<month>\d{2}).(?P<year>\d{4})',
    ]))
parsed_text = ""

def md_export(d):
    global parsed_text # to access the global variable parsed_text
    for book in d:
        parsed_text += "# {}\n".format(book)
        for page in d[book]:
            parsed_text+= "- p{}\n".format(page)
            for note in d[book][page]:
                #[quote, note] if note else [page, quote]
                parsed_text+= "\t- > {}\n".format(note[0])
                if len(note) > 1: # then there's a note
                    parsed_text+= "\t\t- [[highlight/note]] {}\n".format(note[1])
        parsed_text += delim +"\n"
    return parsed_text

def write_to_file(t):
    with open("output.txt", 'w+') as f:
        f.write(t)

def sanitize(unit):
    a = re.sub('^\n','', unit)
    b = re.sub('\s{2,}',' ', a)
    return b

def main():
    d = {}
    # Parsing notes.txt
    with open("real_notes.txt") as f:
        text = f.read()
        #text = text.replace(u'\xa0', u' ')
        #text = re.sub('^\s*',"", text)
    blocks = text.split(delim)
    for block in blocks:
        m = block_re.search(block)
        if m:
            book = m.group("title")
            page = m.group("page")
            quote = sanitize(m.group("quote"))
            note = m.group("note")
            if book in d.keys():
                if page in d[book]:
                    d[book][page].append([quote,note] if note else [quote])
                else:
                    d[book][page] = [[quote, note]] if note else [[quote]]
            else:
                d[book] = {page: [[quote, note]]} if note else {page: [[quote]]} #[[page, quote, note] if note else [page, quote]]
    print(md_export(d))
    #write_to_file(md_export(d))

if(__name__=="__main__"):
    main()
