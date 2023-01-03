import xlrd
import agate
from xlrd.sheet import ctype_text
import numpy
import agatestats
import json

"""
Activity 1 Importing
"""
workbook = xlrd.open_workbook('unicef_oct_2014.xls')
workbook.nsheets
workbook.sheet_names()

sheet = workbook.sheets()[0]
sheet.nrows
sheet.row_values(0)


for r in range(sheet.nrows):
    print (r, sheet.row(r))


title_rows = zip(sheet.row_values(4), sheet.row_values(5))
title_rows

titles = [t[0] + ' ' + t[1] for t in title_rows] ## spacing
titles = [t.strip() for t in titles]
titles

country_rows = [sheet.row_values(r) for r in range(6, 114)]
country_rows

##Activity 1.1
text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()

example_row = sheet.row(6)
print (example_row)
print (example_row[0].ctype)
print (example_row[0].value)
print (ctype_text)

##Activity 1.2

types = []

for v in example_row:

    value_type = ctype_text[v.ctype]

    if value_type == 'text':
        types.append(text_type)
    elif value_type == 'number':
        types.append(number_type)
    elif value_type == 'xldate':
        types.append(date_type)
    else:
        types.append(text_type)


types
titles

def remove_bad_chars(val):
    if val == '-':
        return None
    return val

cleaned_rows = []

for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)


table = agate.Table(cleaned_rows, titles, types)
table

def get_new_array (old_aray, function_to_clean):
    new_arr = []

    for row in old_aray:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr


cleaned_rows = get_new_array(country_rows, remove_bad_chars)

table = agate.Table(cleaned_rows, titles, types)
table.print_table(max_columns=7)
table.column_names


"""
Activity 2 Exploring the Data

"""

most_egregious = table.order_by('Total (%)', reverse=True).limit(10)


for r in most_egregious.rows:
    print (r)

most_females = table.order_by('Female', reverse=True).limit(10)


for r in most_females.rows:
    print ('{}: {}%'.format(r['Countries and areas'], r['Female']))


female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse=True).limit(10)

for r in most_females.rows:
    print ('{}: {}%'.format(r['Countries and areas'], r['Female']))

(lambda x: 'Positive' if x >= 1 else 'Zero or Negative')(0)
(lambda x: 'Positive' if x >= 1 else 'Zero or Negative')(4)


has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
has_por.aggregate(agate.Mean('Place of residence (%) Urban'))

first_match = has_por.find(lambda x: x['Rural'] > 50)
first_match['Countries and areas']


ranked = table.compute([('Total Child Labor Rank', agate.Rank('Total (%)', reverse=True)),])


for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print (row['Total (%)'], row['Total Child Labor Rank'])


def reverse_percent(row):
    return 100 - row['Total (%)']

ranked = table.compute([('Children not working (%)',agate.Formula(number_type, reverse_percent)),])
ranked = ranked.compute([('Total Child Labor Rank',agate.Rank('Children not working (%)')),])


for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print (row['Total (%)'], row['Total Child Labor Rank'])



"""
Activity 3 Joining Data
"""

cpi_workbook = xlrd.open_workbook('corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

for r in range (cpi_sheet.nrows):
    print (r, cpi_sheet.row_values(r))


cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]
cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]


def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print (e)

def get_types(example_row):
    types = []

    for v in example_row:
        value_type = ctype_text[v.ctype]

        if value_type == 'text':
            types.append (text_type)
        elif value_type == 'number':
            types.append (number_type)
        elif value_type == 'xldate':
            types.append (date_type)
        else:
            types.append (text_type)
    return types


cpi_types = get_types(cpi_sheet.row(3))
cpi_titles
cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

cpi_titles[0] = cpi_titles[0] + ' Duplicate'

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory', 'Countries and areas', inner=True)

cpi_and_cl.print_table()
cpi_and_cl.column_names
len(cpi_and_cl.rows)
len(cpi_table.rows)
len(ranked.rows)


for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print ('{}: {} - {}%'.format(r['Country / Territory'],r['CPI 2013 Score'], r['Total (%)']))


numpy.corrcoef([float(t) for t in cpi_and_cl.columns['Total (%)'].values()],[float(s) for s in cpi_and_cl.columns['CPI 2013 Score'].values()])[0,1]

std_dev_outliers = cpi_and_cl.stdev_outliers('Total (%)', deviations=3, reject=False)
len(std_dev_outliers.rows)

std_dev_outliers=cpi_and_cl.stdev_outliers('Total (%)', deviations=5, reject=False)
len(std_dev_outliers.rows)

mad = cpi_and_cl.mad_outliers('Total (%)')

for r in mad.rows:
    print (r['Country / Territory'], r['Total (%)'])


"""
Aggregating data
"""

country_json = json.loads(open('earth.json', 'rb').read())

country_dict = {}

for dct in country_json:
    country_dict[dct['name']] = dct['parent']

def get_country(country_row):
    return country_dict.get(country_row['Country / Territory'].lower())

cpi_and_cl = cpi_and_cl.compute([('continent', agate.Formula(text_type, get_country)),])
cpi_and_cl.column_names

for r in cpi_and_cl.rows:
    print(r['Country / Territory'], r['continent'])


no_continent = cpi_and_cl.where(lambda x: x['continent'] is None)

for r in no_continent.rows:
    print (r['Country / Territory'])


cpi_and_cl = cpi_table.join (ranked, 'Country / Territory', 'Countries and areas', inner=True)

country_json = json.loads(open('earth-cleaned.json', 'rb').read())


for dct in country_json:
    country_dict[dct['name']] = dct['parent']

cpi_and_cl = cpi_and_cl.compute([('continent', agate.Formula(text_type, get_country)),])


for r in cpi_and_cl.rows:
    print (r['Country / Territory'], r['continent'])


grp_by_cont = cpi_and_cl.group_by('continent')
grp_by_cont

for cont, table in grp_by_cont.items():
    print (cont, len(table.rows))



agg = grp_by_cont.aggregate([('cl_mean', agate.Mean('Total (%)')),
                                ('cl_max', agate.Max('Total (%)')),
                                ('cpr_median',agate.Median('CPI 2013 Score')),
                                ('cpi_min',agate.Min('CPI 2013 Score'))])

agg
agg.print_table()


agg.print_bars('continent', 'cl_max')

"""
Activity 5 Final
Seprating and Focusing Data
"""


africa_cpi_cl = cpi_and_cl.where(lambda x: x['continent'] == 'africa')

for r in africa_cpi_cl.order_by('Total (%)', reverse=True).rows:
    print ('{}: {}% - {}'.format(r['Country / Territory'], r['Total (%)'], r['CPI 2013 Score']))

print (numpy.corrcoef ([float(t) for t in africa_cpi_cl.columns['Total (%)'].values()],[float(c) for c in africa_cpi_cl.columns['CPI 2013 Score'].values()])[0,1])

africa_cpi_cl = africa_cpi_cl.compute ([('Africa Child Labor Rank', agate.Rank('Total (%)', reverse=True)),])
africa_cpi_cl = africa_cpi_cl.compute ([('Africa OPT Rank', agate.Rank('CPI 2013 Score')),])


africa_cpi_cl.print_table()


cpi_mean = africa_cpi_cl.aggregate(agate.Mean('CPI 2013 Score'))
cl_mean = africa_cpi_cl.aggregate(agate.Mean('Total (%)'))

cl_mean
cpi_mean



def highest_rates(row):
    if row ['Total (%)'] > cl_mean and row['CPI 2013 Score'] < cpi_mean:
        return True
    return False



highes_cpi_cl = africa_cpi_cl.where(lambda x: highest_rates(x))

for r in highes_cpi_cl.rows:
    print ('{}: {}% - {}'.format(r['Country / Territory'], r['Total (%)'], r['CPI 2013 Score']))

