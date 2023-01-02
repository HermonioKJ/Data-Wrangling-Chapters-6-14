from lxml import html

with open(r'data\chp11\take_action_enough_project.html', 'r') as f:
    contents = f.read()

doc = html.document_fromstring(contents)
ta_divs = doc.cssselect('div.views-row')

print(ta_divs)

all_data = []

for ta in ta_divs:
    data_dict = {}
    title = ta.cssselect('h2')[0]
    data_dict['title'] = title.text_content()
    data_dict['link'] = title.find('a').get('href')
    data_dict['about'] = [p.text_content() for p in ta.cssselect('p')]
    all_data.append(data_dict)

print(all_data)

#

print(doc.find('div'))
print(doc.find('head'))
print(doc.find('head').findall('script'))
print(doc.cssselect('div'))
print(doc.cssselect('head script'))
