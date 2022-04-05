import re

#delimetor between not blocks
delim = "-----------------------------------"

#regex for a note block
block_re = re.compile(r'\n'.join([
    r'(?P<title>.+)',
    r'((?P<type>Lesezeichen|Markierung|Notiz)\sauf\sSeite\s(?P<page>\d+):\s)' + r'''((?P<note>(?:.|\n)*))?''' + r'"(?P<quote>(?:.|\n)*)"',
    r'(Hinzugefügt|Geändert)\sam\s(?P<day>\d{2}).(?P<month>\d{2}).(?P<year>\d{4})',
    ]))

def main():
    d = {}
    with open("notes.txt") as f:
        text = f.read()
        #text = text.replace(u'\xa0', u' ')
        #text = re.sub('^\s*',"", text)
    blocks = text.split(delim)
    for block in blocks:
        m = block_re.search(block)
        if m:
            book = m.group("title")
            page = m.group("page")
            quote = m.group("quote")
            note = m.group("note")
            if book in d.keys():
                d[book].append([page, quote, note]) if note else d[book].append([page, quote])
            else:
                d[book] = [[page, quote, note] if note else [page, quote]]
        print(d)

if(__name__=="__main__"):
    main()
