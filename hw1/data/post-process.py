# Simple post-processing script to create a clean subset of tree data
#     - JRz, for personal use and not indended for real-world applications
 
#  NOTE: This is eliminating valid, useful data in lieu of something easier to visualize
#        It's possible that this will mask trends, as it is often VERY likely that missing data are non-randomly distributed (e.g. more missing data pre-1955 in this dataset)


import csv

import googlemaps
from tqdm import tqdm
from pprint import pp
import re

gmaps = googlemaps.Client(key='AIzaSyBRd-GJnghzCYXiHEZJ3bvXySphFYhUlk8')

def passes_filter(row):
    # Filter criteria:
    #   Only listed trees that have full species name supplied
    if len(row['qSpecies']) < 3 or 'Tree(s) ::' in row['qSpecies']:
        return False
    #   Only trees that have a lat and lng provided
    elif len(row['Latitude']) < 2 or len(row['Longitude']) < 2:
        return False
    #   Only trees with valid SiteInfo
    elif len(row['qSiteInfo']) < 1 or row['qSiteInfo'] == ':':
        return False
    #   Only trees that have a DBH provided
    elif len(row['DBH']) < 1:
        return False
    else:
        return True
    
    # think about what other filters you could run here...

def find_postal(address_components):
    for item in address_components:
        if item['types'][0] == 'postal_code':
            return int(item['long_name'])

# import and run passes_filter
data = []
header = []
with open('Street_Tree_List-2022-01-30_RAW.csv','r') as f:
    reader = csv.DictReader(f)
    
    header = reader.fieldnames
    header.append('PostalCode')
    print(header)
    for row in tqdm(reader):
        if passes_filter(row):
            # you might consider doing some additional processing here
            # e.g. splitting up qSpecies
            
            postal_code = find_postal(reversed(gmaps.reverse_geocode(
                (row['Latitude'], row['Longitude']))[0]['address_components']))
            
            row['PostalCode'] = postal_code            
            data.append(row)

print(len(data))

# export to new CSV       
with open('Street_Tree_List-2022-01-30_FILTERED.csv','w') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)

# median income data
asthma_dict =  {'94102': 12.97,
                '94103': 10.57,
                '94107': 4.68,
                '94108': 3.64,
                '94109': 3.82,
                '94110': 6.74,
                '94112': 4.48,
                '94114': 3.08,
                '94115': 5.45,
                '94116': 2.5,
                '94117': 3.65,
                '94118': 1.92,
                '94121': 2.71,
                '94122': 2.81,
                '94124': 16.12,
                '94127': 2.7,
                '94131': 1.95,
                '94132': 3.95,
                '94133': 5.06,
                '94134': 7.5}

data = []
with open('Census_Median_Income-2022.csv', 'r') as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames

    for name in range(len(header)):
        header[name] = (re.findall(r'\d+', header[name])[1])

    
    for row in reader:
        data.append(row)
    data.append(asthma_dict)

with open('Census_Median_Income-2022_FILTERED.csv','w') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(data)
