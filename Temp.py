"""Get Wikidata dump records as a JSON stream (one JSON object per line)"""
# Modified script taken from this link: "https://www.reddit.com/r/LanguageTechnology/comments/7wc2oi/does_anyone_know_a_good_python_library_code/dtzsh2j/"
import bz2
import json
import pandas as pd
import pydash

def wikidata(filename):
    with bz2.open(filename, mode='rt') as f:
        f.read(2)  # skip first two bytes: "[\n"
        for line in f:
            try:
                yield json.loads(line.rstrip(',\n'))
            except json.decoder.JSONDecodeError:
                continue

def getLocations(WikiDumpFilepath, folderOut):
    i = 0
    import os
    if not os.path.isdir(folderOut):
        os.mkdir(folderOut)

    for record in wikidata(WikiDumpFilepath):
        # only extract items with geographical coordinates (P625)
        if pydash.has(record, 'claims.P625'):
            #print('i = ' + str(i) + ' item ' + record['id'] + '  started!' + '\n')
            latitude = pydash.get(record, 'claims.P625[0].mainsnak.datavalue.value.latitude')
            longitude = pydash.get(record, 'claims.P625[0].mainsnak.datavalue.value.longitude')
            english_label = pydash.get(record, 'labels.en.value')
            item_id = pydash.get(record, 'id')
            item_type = pydash.get(record, 'type')
            english_desc = pydash.get(record, 'descriptions.en.value')
            df_record = pd.DataFrame(
                {'id': item_id, 'type': item_type, 'english_label': english_label, 'longitude': longitude,
                 'latitude': latitude, 'english_desc': english_desc}, index=[i])
            df_record_all = df_record_all.append(df_record, ignore_index=True)
            i += 1
            #print(i)
            if (i % 5000 == 0):
                pd.DataFrame.to_csv(df_record_all,
                                    path_or_buf=folderOut + record['id'] + '_item.csv')
                print('i = ' + str(i) + ' item ' + record['id'] + '  Done!')
                print('CSV exported')
                df_record_all = pd.DataFrame(
                    columns=['id', 'type', 'english_label', 'longitude', 'latitude', 'english_desc'])
            else:
                continue
    pd.DataFrame.to_csv(df_record_all,
                        path_or_buf=folderOut + record['id'] + '_item.csv')
    #print('i = ' + str(i) + ' item ' + record['id'] + '  Done!')
    print('All items finished, final CSV exported!')

if __name__ == '__main__':

    if True:
        import os
        import datetime
        folderOut = 'Wiki/'
        if not os.path.isdir(folderOut):
            os.mkdir(folderOut)
        WikiDumpFilepath = '/media/aleksei1985/Seagate Expansion Drive/WikiKGTK/latest-all2.json.bz2'

        i = 0
        docCount = 0
        df_record_all = pd.DataFrame(columns=['id', 'english_label', 'english_desc', 'num_sitelinks', 'Twitter_Screen_Name', 'Twitter_ID', 'Twitter_Follows', 'coordinates', 'types'])
        for record in wikidata(WikiDumpFilepath):
            #items not used
            #aliases = alternative names
            #lastrevid = last time revised not clear what it stands for i.e. does not seem to be in seconds
            #type (item for most)

            #explanations
            #claims are of most interest
            #sitelinks = https://www.wikidata.org/wiki/Help:Sitelinks
            #(Sitelinks serve as a replacement for a previous system of interlanguage links that was used to link from a page in one language on a Wikimedia site to an equivalent page in another language, for example the English Wikipedia page on Paris to the French Wikipedia page on Paris)
            #the more sitelinks the more popular a concept since there are corresponding items in different languages
            if pydash.has(record, 'claims.P2002'): #P2002 = Twitter Name
                wikiData_ID = record["id"]
                if (wikiData_ID == '11Q640111'):
                    print(record)
                    for claim in record["claims"]:
                        print(claim)
                    english_desc = pydash.get(record, 'descriptions.en.value')
                    print(english_desc)
                    import sys
                    sys.exit()

                english_label = pydash.get(record, 'labels.en.value')
                english_desc = str(pydash.get(record, 'descriptions.en.value'))
                num_sitelinks = len(record["sitelinks"])

                Twitter_Screen_Name = pydash.get(record, 'claims.P2002[0].mainsnak.datavalue.value')
                Twitter_ID = str(pydash.get(record, 'claims.P2002[0].qualifiers.P6552[0].datavalue.value')) # numeric Twitter id
                Twitter_Follows = pydash.get(record, 'claims.P2002[0].qualifiers.P3744[0].datavalue.value.amount') #followers

                coordinates = ""
                if pydash.has(record, 'claims.P625'): #location
                    latitude = str(pydash.get(record, 'claims.P625[0].mainsnak.datavalue.value.latitude'))
                    longitude = str(pydash.get(record, 'claims.P625[0].mainsnak.datavalue.value.longitude'))
                    coordinates = "(" + latitude + ", " + longitude + ")"

                types = ""
                if pydash.has(record, 'claims.P31'): #instance of
                    P31Types = []
                    for types in record["claims"]["P31"]:
                        P31Types.append(types["mainsnak"]["datavalue"]["value"]["id"])
                    types = str(P31Types)
                    # example P31 types: Q5 = human, Q207694 = art museum, Q1549591 = big city, etc.

                df_record = pd.DataFrame({'id': wikiData_ID, 'english_label': english_label, 'english_desc': english_desc,
                     'num_sitelinks': num_sitelinks, 'Twitter_Screen_Name': Twitter_Screen_Name, 'Twitter_ID': Twitter_ID,
                    'Twitter_Follows':Twitter_Follows, 'coordinates': coordinates, 'types': types}, index=[i])
                df_record_all = df_record_all.append(df_record, ignore_index=True)

                i += 1
                # print(i)
                if (i % 50 == 0):
                    pd.DataFrame.to_csv(df_record_all, path_or_buf=folderOut + str(docCount) + '_item.csv')
                    print('i = ' + str(i) + ' item ' + record['id'] + '  Done!')
                    print('CSV exported')
                    df_record_all = pd.DataFrame(columns=['id', 'english_label', 'english_desc', 'num_sitelinks', 'Twitter_Screen_Name', 'Twitter_ID', 'Twitter_Follows', 'coordinates', 'types'])
                    docCount += 1
                else:
                    continue
        pd.DataFrame.to_csv(df_record_all, path_or_buf=folderOut + record['id'] + '_item.csv')
        print('i = ' + str(i) + ' item ' + record['id'] + '  Done!')
        print('All items finished, final CSV exported!')
