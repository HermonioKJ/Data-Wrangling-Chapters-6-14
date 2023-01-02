from bs4 import BeautifulSoup

with open(r'data\chp11\take_action_enough_project.html', 'r') as f:
    contents = f.read()

bs = BeautifulSoup(contents)

ta_divs = bs.find_all('div', class_='views-row')

print(len(ta_divs))

for ta in ta_divs:
    title = ta.h2
    link = ta.a
    about = ta.find_all('p')
    print('\n\nTITLE\n', title)
    print('\n\nLINK\n', link)
    print('\n\nABOUT\n', about)

#

all_data = []

for ta in ta_divs:
    data_dict = {}
    data_dict['title'] = ta.h2.get_text()
    data_dict['link'] = ta.a.get('href')
    data_dict['about'] = [p.get_text() for p in ta.find_all('p')]
    all_data.append(data_dict)

print('\n\nALL DATA\n', all_data)
