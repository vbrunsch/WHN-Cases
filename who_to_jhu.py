import pandas as pd
import numpy as np

# Get case time series from JHU
#jhu = pd.read_csv('jhu.csv')
jhu = pd.read_csv(f'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv?raw=true')
#print(jhu)

# Get data from WHO
who = pd.read_csv(f'https://covid19.who.int/WHO-COVID-19-global-data.csv')
#print(who)

# select only the columns we need
wh = who[['Date_reported', 'Country', 'Cumulative_cases']]

# transpose wh to match JHU
wh = wh.pivot(index='Country', columns='Date_reported', values='Cumulative_cases')

# change date in column names to match JHU
wh.columns = pd.to_datetime(wh.columns, format='%Y-%m-%d')
wh.columns = wh.columns.strftime('%m/%d/%y')

# change column names of dates no leading zero
wh.columns = wh.columns.str.replace(r'(\d+)/0(\d+)/(\d+)', r'\1/\2/\3')
wh.columns = wh.columns.str.replace(r'0(\d+)/(\d+)/(\d+)', r'\1/\2/\3')
wh['Country/Region'] = wh.index
wh = wh.reset_index(drop=True)

# change entries in wh country/region
wh['Country/Region'] = wh['Country/Region'].replace({'Bolivia (Plurinational State of)': 'Bolivia',
                'Myanmar': 'Burma',
                'Brunei Darussalam': 'Brunei',
                'Congo': 'Congo (Brazzaville)',
                'Côte d’Ivoire': 'Cote d\'Ivoire',
                'Iran (Islamic Republic of)': 'Iran',
                'Democratic People\'s Republic of Korea': 'Korea, North',
                'Republic of Korea': 'Korea, South',
                'Kosovo[1]': 'Kosovo',
                'Lao People\'s Democratic Republic': 'Laos',
                'Micronesia (Federated States of)': 'Micronesia',
                'Republic of Moldova': 'Moldova',
                'Russian Federation': 'Russia',
                'Syrian Arab Republic': 'Syria',
                'The United Kingdom': 'United Kingdom',
                'United Republic of Tanzania': 'Tanzania',
                'United States of America': 'US',
                'Türkiye': 'Turkey',
                'Venezuela (Bolivarian Republic of)': 'Venezuela',
                'Viet Nam': 'Vietnam'})
#print(wh)

#delete first 19 columns
wh = wh.iloc[:, 19:]
#print(wh)

# find entries in wh country region that are also in jhu country region
wh_in_jhu = wh[wh['Country/Region'].isin(jhu['Country/Region'])]
#print(wh_in_jhu)

# find entries in jhu country region that are not in the new wh_in_jhu country region
jhu_not_in_wh_new = jhu[~jhu['Country/Region'].isin(wh_in_jhu['Country/Region'])]
#print(jhu_not_in_wh_new)

# add rows from jhu_not_in_wh_new to wh_in_jhu
wh_in_jhu = wh_in_jhu.append(jhu_not_in_wh_new)
#print(wh_in_jhu)

# add rows with entries in jhu province/state column to wh_in_jhu
wh_in_jhu = wh_in_jhu.append(jhu[jhu['Province/State'].notnull()])

# sort alphabetically by country/region, then by province/state, then reindex
wh_in_jhu = wh_in_jhu.sort_values(by=['Country/Region', 'Province/State']).reset_index(drop=True)

# sort columns so that province/state is first, then country/region, then Lat, Long, then dates
wh_in_jhu = wh_in_jhu[['Province/State', 'Country/Region', 'Lat', 'Long'] + list(wh_in_jhu.columns[0:-4])]

# replace row 61 with row 95 and delete row 95, then replace row 41 with row 57 and delete row 57, then replace row 9 with row 17 and delete row 17
# as there are no entries for Australia, Canada and China apart from the province data
wh_in_jhu.iloc[61] = wh_in_jhu.iloc[95]
wh_in_jhu = wh_in_jhu.drop(95)
wh_in_jhu.iloc[41] = wh_in_jhu.iloc[57]
wh_in_jhu = wh_in_jhu.drop(57)
wh_in_jhu.iloc[9] = wh_in_jhu.iloc[17]
wh_in_jhu = wh_in_jhu.drop(17).reset_index(drop=True)
wh_in_jhu.to_csv('who_new.csv')
