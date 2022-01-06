import pandas as pd
import pydash

def gettingResultsWithoutTools():
    query = '''
            SELECT (COUNT (distinct ?x) AS ?count)
            WHERE
            {
              ?x wdt:P2002 ?twitterName
            }
            '''

    import requests
    url = 'https://query.wikidata.org/sparql'
    r = requests.get(url, params={'format': 'json', 'query': query})
    if '200' in str(r):
        data = r.json()
        print(data)


def executeWikiQuery(query):
    import requests
    import time

    url = 'https://query.wikidata.org/sparql'
    r = requests.get(url, params={'format': 'json', 'query': query})
    if '200' in str(r):
        data = r.json()
        return data
    elif '429' in str(r):
        #too many requests wait and try again in 5 minutes
        import time
        print("sleeping for 5 minutes")
        time.sleep(300)
        return executeWikiQuery(query)
    else:
        print("Error processing request")
        print(r)
        import sys
        sys.exit()

def getAllWikiDataPropertiesSPARQLQuery():
    query = '''
    SELECT ?property ?propertyLabel ?propertyDescription (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {
        ?property a wikibase:Property .
        OPTIONAL { ?property skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "en") }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" .}
    }
    GROUP BY ?property ?propertyLabel ?propertyDescription
    '''

    return query

def getAllPropertiesFile():
    folderOut = 'Wiki/'

    df_record_all = pd.DataFrame(
        columns=['property', 'propertyLabel', 'propertyDescription', 'altLabel_list'])

    data = executeWikiQuery(getAllWikiDataPropertiesSPARQLQuery())

    columns = data["head"]
    results = data["results"]["bindings"]
    i = 0
    for property in results:
        df_record = pd.DataFrame(
            {'property': pydash.get(property, 'property.value'),
             'propertyLabel': pydash.get(property, 'propertyLabel.value'),
             'propertyDescription': pydash.get(property, 'propertyDescription.value'),
             'altLabel_list': pydash.get(property, 'altLabel_list.value')}, index=[i])
        df_record_all = df_record_all.append(df_record, ignore_index=True)
        i += 1

    pd.DataFrame.to_csv(df_record_all, path_or_buf=folderOut + 'WikiDataProperties.csv')

def getPropertyUsagePerTwitterUser(inpath):
    import time
    folderOut = 'Wiki/'

    import pandas as pd
    df = pd.read_csv(inpath, encoding='utf-8')
    properties = df["property"]
    propertyUsage = []
    i = 0

    for property in properties:
        property = property.split("/")[-1]

        query = '''
        SELECT (COUNT (distinct ?x) AS ?count)
        WHERE
        {
          ?x wdt:P2002 ?twitterName;
             wdt:''' +str(property) + '''?id
        }
        '''

        count = queryWikiDirectlyForPropertyCount(property, query)
        print(str(i) + ", " + str(count) + ", " + property)
        propertyUsage.append(count)
        i += 1
        time.sleep(2)

    df["propertyUsage"] = propertyUsage
    pd.DataFrame.to_csv(df, path_or_buf=folderOut + 'WikiDataPropertiesPerPerson2.csv')

def queryWikiDirectlyForPropertyCount(property, queryInput):
    import requests
    import time

    url = 'https://query.wikidata.org/sparql'
    query = queryInput
    if query == None:
        query = '''
        SELECT (COUNT (distinct ?x) AS ?count)
        WHERE
        {
          ?x wdt:''' +str(property) + '''?id
        }
        '''

    #print(query)
    r = requests.get(url, params={'format': 'json', 'query': query})
    #print(r)
    if '200' in str(r):
        data = r.json()
        return data['results']['bindings'][0]['count']['value']
    elif '429' in str(r):
        #too many requests wait and try again in 5 minutes
        import time
        print("sleeping for 5 minutes")
        time.sleep(300)
        return queryWikiDirectlyForPropertyCount(property, queryInput)
    else:
        print("Error processing request")
        print(r)
        import sys
        sys.exit()

def recordSocialSiteInfo():
    import time
    folderOut = 'Wiki/'
    socialMediaSites = ['P2002', 'P2003', 'P2013', 'P2037', 'P2397', 'P2847', 'P2893', 'P2942', 'P2984', 'P3040',
                        'P3185', 'P3207', 'P3258', 'P3267', 'P3502', 'P3579', 'P3789', 'P3836', 'P3899', 'P3943',
                        'P4003', 'P4013', 'P4015', 'P4016', 'P4017', 'P4033', 'P4174', 'P4175', 'P4226', 'P4264',
                        'P4265', 'P4411', 'P5163', 'P5434', 'P5435', 'P5797', 'P6450', 'P6451', 'P6455', 'P6459',
                        'P6552', 'P6837', 'P7085', 'P7171', 'P7211', 'P7590', 'P7737', 'P8527', 'P8754', 'P8827',
                        'P8842', 'P8904', 'P8919', 'P8976', 'P9101', 'P9269', 'P9271', 'P9509', 'P9812', 'P9928',
                        'P9934'] #based on query ?x wdt:P31 wd:Q105388954.
    df_record_socialMediaSite = pd.DataFrame(
        columns=['id', 'number sites'])
    i = 0
    for socialMediaSiteID in socialMediaSites:
        df_record = pd.DataFrame(
            {'id': socialMediaSiteID, 'number sites': queryWikiDirectlyForPropertyCount(socialMediaSiteID, None)},
            index=[i])
        df_record_socialMediaSite = df_record_socialMediaSite.append(df_record, ignore_index=True)
        time.sleep(2)
        i += 1

    pd.DataFrame.to_csv(df_record_socialMediaSite, path_or_buf=folderOut + 'socialSites2.csv')

if __name__ == '__main__':
    gettingResultsWithoutTools()

    #recordSocialSiteInfo()

    folderOut = 'Wiki/'
    inpath = folderOut + 'WikiDataProperties.csv'
    #getPropertyUsagePerTwitterUser(inpath)
