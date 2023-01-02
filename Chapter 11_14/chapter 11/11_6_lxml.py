from lxml import html

with open(r'data\chp11\emoji_cheat_sheet.html', 'r', encoding='utf-8') as f:
    contents = f.read()

page = html.document_fromstring(contents)

body = page.find('body')
top_header = body.find('h2')
print('\n\nTOP HEADER TEXT\n', top_header.text)

headers_and_lists = [sib for sib in top_header.itersiblings()]

print(headers_and_lists)

proper_headers_and_lists = [s for s in top_header.itersiblings() if s.tag in [
    'ul', 'h2', 'h3']]

print(proper_headers_and_lists)
