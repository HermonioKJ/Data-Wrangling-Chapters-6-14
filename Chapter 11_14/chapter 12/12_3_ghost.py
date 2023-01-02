# Ghost module DEPRECATED/UNMAINTAINED

"""from ghost import Ghost

ghost = Ghost()
with ghost.start() as session:
    page, extra_resources = session.open('http://python.org')
    print(page)
    print(page.url)
    print(page.headers)
    print(page.http_status)
    print(page.content)
    print(extra_resources)
    for r in extra_resources:
        print(r.url)

print(page.content.contains('input'))

result, resources = session.evaluate(
    'document.getElementsByTageName("input");')

print(result.keys())
print(result.get('length'))
print(resources)
"""
