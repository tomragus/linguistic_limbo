# Treading... into the world of languages

# importing countries & codes dataset

import pandas as pd

# reading the pre-processed countries dataset
df_countries = pd.read_csv('path/to/countries_codes_and_coordinates_(clean).csv')

# removing quotations and spaces from country codes
# dset = dataset
# col = column you want to clean
def cleancodes(dset, col):
    for i in range(0, len(dset)):
        alph = dset.iloc[i, col]
        alph = alph.replace('"', '')
        alph = alph.replace(' ', '')
        dset.iloc[i, col] = alph
        
cleancodes(df_countries, 0)
cleancodes(df_countries, 1)


# reading the language atlas dataset
df_lang_atlas = pd.read_csv('path/to/language_atlas_(clean).csv')

# removing multiple country codes
# dset = dataset
# col = column you want to clean
# length = how long the output string should be
def shortenstrings(dset, col, length):
    for i in range(len(dset)):
        c_code = (dset.iloc[i,col])[:length]
        dset.iloc[i,col] = c_code

shortenstrings(df_lang_atlas, 1, 2)


# filling the country and alpha-3 codes into language atlas dataset
def fillcountry(dset, given):
    global df_countries
    elems = [0, 1, 2]
    elems.remove(given)
    for i in range(0, len(dset)):
        var = dset.iloc[i,given]
        for j in range(0, len(df_countries)):
            if var == df_countries.iloc[j,given]:
                for k in elems:
                    new = df_countries.iloc[j,k]
                    dset.iloc[i,k] = new
                break
        
fillcountry(df_lang_atlas, 1)
    
# reading the endangered dataset
df_endangeredlangs = pd.read_csv('path/to/endangered_langs_dataset_(clean).csv')    

# removed null rows columns from endangered dataset

# removing extra country and ISO codes
shortenstrings(df_endangeredlangs, 0, 3)
shortenstrings(df_endangeredlangs, 6, 3)

# filling the country and alpha-2 codes into language atlas dataset
fillcountry(df_endangeredlangs, 0)

# clean up datasets
df_endangeredlangs.iloc[332, 3]="Hoa"
df_endangeredlangs.iloc[333, 3]="Ani"
df_endangeredlangs.iloc[334, 3]="Gana"
df_endangeredlangs.iloc[335, 3]="Ku'e"
df_endangeredlangs.iloc[336, 3]="Xegwi"
df_endangeredlangs.iloc[655, 3]="Geta"
df_lang_atlas.iloc[967,3]="Ju'hoan"

# removed null rows
# endangered: rows 234, 274, 278, 924, 1112, 1179, 1488
# atlas: rows 1849, 1876, 2569

# assign "region" to countries in endangered dataset using atlas dataset
def fillregion(dset):
    global df_lang_atlas
    for i in range(0, len(dset)):
        var = dset.iloc[i,0]
        for j in range(0, len(df_lang_atlas)):
            if var == df_lang_atlas.iloc[j,0]:
                new = df_lang_atlas.iloc[j,8]
                dset.iloc[i,8] = new
                break

fillregion(df_endangeredlangs)

# remove null rows
# all endangered: 195, 203, 237, 488, 603, 742, 802, 805, 806, 928, 
# 1236, 1262, 1495, 1500, 1505, 1518, 1519, 1628, 1651, 1683, 1694, 
# 1698, 1736, 1741, 1787, 1846, 1855, 2236, 2256, 2285, 2301, 2380,
# 2392, 2396, 2421, 2443

# combine the atlas and endengered datasets into a 3rd languages dataset (removing all duplicates)
def combine(dset_1, dset_2):
    atlas_merge = dset_1.iloc[:, 0:9]
    endanger_merge = dset_2.iloc[:, 0:10]
    names = atlas_merge['Names'].tolist()
    atlas_merge['Number of speakers'] = 7500001
    for i in range(0, len(endanger_merge)):
        var = endanger_merge.iloc[i,3]
        if var not in names:
            atlas_merge = pd.concat([atlas_merge, endanger_merge.iloc[[i]]], ignore_index=True)           
    return(atlas_merge)
    
languages = combine(df_lang_atlas, df_endangeredlangs)

# rename df_lang_atlas, df_endangeredlangs and export all as CSV
df_lang_atlas.to_csv('save/path/FINAL_atlas.csv', index = False)
df_endangeredlangs.to_csv('save/path/FINAL_endangered.csv', index = False)
languages.to_csv('save/path/FINAL_lanugages.csv', index = False)


# re-importing datasets (as to not re-create from scratch)
import pandas as pd

atlas = pd.read_csv('path/to/FINAL_atlas.csv')
endangered = pd.read_csv('path/to/FINAL_endangered.csv')
languages = pd.read_csv('path/to/FINAL_lanugages.csv')

# re-import countries dataset (if needed)
df_countries = pd.read_csv('path/to/countries_codes_and_coordinates_(clean).csv')

def cleancodes(dset, col):
    for i in range(0, len(dset)):
        alph = dset.iloc[i, col]
        alph = alph.replace('"', '')
        alph = alph.replace(' ', '')
        dset.iloc[i, col] = alph
        
cleancodes(df_countries, 0)
cleancodes(df_countries, 1)


# import subsets of language dataset (created in Excel) for Eurasia, Papunesia, Africa
df_Eurasia = pd.read_csv('path/to/Languages_Eurasia.csv')
df_Papunesia = pd.read_csv('path/to/Languages_Papunesia.csv')
df_Africa = pd.read_csv('path/to/Languages_Africa.csv')


# create dataframes of all countries in a region with the number of languages in that country
def languages_in_countries(dset):
    countries_all = list(dset.iloc[:,2])
    countries_unique = list(set(dset.iloc[:,2]))
    languages_in_countries = pd.DataFrame({
        'Country': countries_unique,
        'Languages per country': [0]*len(countries_unique)
        })
    for i in range(0, len(countries_unique)):
        languages_in_countries.iloc[i,1] = countries_all.count(countries_unique[i])
    return(languages_in_countries)

bycountry_Eurasia = languages_in_countries(df_Eurasia)
bycountry_Papunesia = languages_in_countries(df_Papunesia)
bycountry_Africa = languages_in_countries(df_Africa)


# export all as CSV      
bycountry_Eurasia.to_csv('save/path/bycountry_Eurasia.csv', index = False)
bycountry_Papunesia.to_csv('save/path/bycountry_Papunesia.csv', index = False)
bycountry_Africa.to_csv('save/path/bycountry_Africa.csv', index = False)


# import modified sheet of Brazil's endangered languages and shift points to first quarter
import pandas as pd

brazil_endangered = pd.read_csv('path/to/Spread Brazil (endangered).csv')
brazil_endangered['Latitude'] = brazil_endangered['Latitude'] + 30.1451
brazil_endangered['Longitude'] = brazil_endangered['Longitude'] + 73.4765


# remove extra null column

# create arrays for each level of endangerment
import numpy as np

vuln_array = brazil_endangered[['Latitude', 'Longitude']].iloc[75:162].values
def_end_array = brazil_endangered[['Latitude', 'Longitude']].iloc[37:47].values
sev_end_array = brazil_endangered[['Latitude', 'Longitude']].iloc[58:74].values
crit_end_array = brazil_endangered[['Latitude', 'Longitude']].iloc[:36].values
extinct_array = brazil_endangered[['Latitude', 'Longitude']].iloc[48:57].values


# ALTERED K-MEANS: calculate centroid for each level of endangerment
def calc_centroid(array):
    lats = array[:,0]
    longs = array[:,1]
    centroid = np.array([[np.mean(lats), np.mean(longs)]])
    return(centroid)

centr1 = calc_centroid(vuln_array)
centr2 = calc_centroid(def_end_array)
centr3 = calc_centroid(sev_end_array)
centr4 = calc_centroid(crit_end_array)
centr5 = calc_centroid(extinct_array)


# generate plot with points for each level of endangerment and centroids
import matplotlib.pyplot as plt

levels_of_endangerment = [vuln_array, def_end_array, sev_end_array, crit_end_array, extinct_array]
colors = ['green', 'blue', 'yellow', 'red', 'black']
centroids = [centr1, centr2, centr3, centr4, centr5]
labels = ['Vulnerable', 'Definitely Endangered', 'Severely Endangered', 'Critically Endangered', 'Extinct']

plt.close('all')
%matplotlib qt

for i in range(0, 5):
    level = levels_of_endangerment[i]
    center = centroids[i]
    lats = level[:, 0]
    longs = level[:, 1]
    plt.scatter(lats, longs, color=colors[i])
    plt.scatter(center[0,0], center[0,1], color=colors[i], marker='*', s = 300, label=labels[i])
plt.title("Centroids (Stars) for each Level of Endangerment")
plt.xlabel("Latitude (Shifted +73)")
plt.ylabel("Longitude (Shifted +30)")
plt.legend()
plt.show()
    
    
# create dataframe of centroids and shift back down to true location
df_centroids = pd.DataFrame({
    'Level of Endangerment': ['Vulnerable', 'Definitely Endangered', 'Severely Endangered', 'Critically Endangered', 'Extinct'],
    'Latitude': [centr1[0,0], centr2[0,0], centr3[0,0], centr4[0,0], centr5[0,0]],
    'Longitude': [centr1[0,1], centr2[0,1], centr3[0,1], centr4[0,1], centr5[0,1]]
    })

df_centroids['Latitude'] = df_centroids['Latitude'] - 30.1451
df_centroids['Longitude'] = df_centroids['Longitude'] - 73.4765


# export centroids as CSV
df_centroids.to_csv('save/path/centroids.csv', index = False)
