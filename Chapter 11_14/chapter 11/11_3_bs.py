from bs4 import BeautifulSoup

with open(r'data\chp11\take_action_enough_project.html', 'r') as f:
    contents = f.read()

    #page = s.get(r'file:\C:\Users\USER\Documents\Projects\Python\Data Wrangling\Data Wrangling\data\chp11\take_action_enough_project.html')
bs = BeautifulSoup(contents)
# print(source_code)
print(bs.title)

print(bs.find_all('a'))

print(bs.find_all('p'))

#
header_children = [c for c in bs.head.children]

print(header_children)

nav_bar = bs.find(id='globalNavigation')

for d in nav_bar.descendants:
    print(d)

for s in d.previous_siblings:
    print(s)
