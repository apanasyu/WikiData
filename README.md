This page designed to show how to utilize WikiData to gain additional data related to Twitter or other social media accounts. We are using both SPARQL queries and Wikidata json.bz2 dumps (we are working with WikiData without any external libraries so as to illustrate how this can be done directly). The extracted info is stored in MongoDB. We are utilizing the country that the Twitter user is associated with to compare against top 100 users per country from SocialBakers.com (which were collected around 2018 timeframe).

# Social Media Types
We are focussing on Twitter because it is the most popular. See file SPARQLQueryDirectly.py function recordSocialSiteInfo():
All of the Wikidata Property IDs can be found via query: query ?item wdt:P31 wd:Q105388954
![image](https://user-images.githubusercontent.com/80060152/148462393-55e0a641-3771-43eb-bed1-810373489f15.png)

In order to get the number of pages related to P2002 (Twitter) do:

    query = '''
            SELECT (COUNT (distinct ?x) AS ?count)
            WHERE
            {
              ?x wdt:P2002 ?y
            }
            '''

In a similar fashion such query was automatically performed for each platform id: P2013, P2003, and so on to get the table below showing the top most popular social media accounts (queried in November 2021):

        id	Number Wiki Pages	English Label
        P2002	299220	                Twitter username
        P2013	210258	                Facebook ID
        P2003	141707	                Instagram username
        P2397	59033	                YouTube channel ID
        P3040	18269	                SoundCloud ID
        P3502	13269	                Ameblo username
        P4264	8445	                LinkedIn company ID
        P3579	7181	                Sina Weibo user ID
        P2037	7121	                GitHub username
        P3185	6804	                VK ID
        
As the table shows Twitter, Facebook, and Instagram are by far the most popular. The numbers of pages with Social media account fluctuates (SPARQLQueryDirectly.py contains code for automatically repeating these steps).

# Working with WikiData

All of the steps can be executed in WorkWithWikiJSONDump.py (that is our main file).

Step 0: Download the latest WikiData dump as a .json.bz2 file from:
https://dumps.wikimedia.org/wikidatawiki/entities/
This is a 72 GB file as of Jan 6 2022.
Working with file will be done via methods in WorkWithWikiJSONDump.py

Step 1: This step produces a file that now contains only WikiData pages that mention a Twitter user name. A lot of WikiData is related to stars, chemicals, and other info that is not relevant to our use case.

Go through downloaded bz2 file line by line and see if a Twitter person is mentioned (looking for P2002, if we wanted to focus on Facebook would use P2013, for Instagram P2003, and so on):

        WikiOriginalFilepath = '/home/aleksei1985/Downloads/latest-all.json.bz2'
        ModWikiDumpPath = '/home/aleksei1985/Desktop/WikiFiles/TwitterRelatedRecords.json'
        import os
        if not os.path.exists(ModWikiDumpPath):
            i = 0
            with open(ModWikiDumpPath, 'w') as fWrite:
                with bz2.open(WikiOriginalFilepath, mode='rt') as fRead:
                    firstTwoBytes = fRead.read(2)  # skip first two bytes: "[\n"
                    fWrite.write(firstTwoBytes)
                    for line in fRead:
                        try:
                            record = json.loads(line.rstrip(',\n'))
                            if pydash.has(record, 'claims.P2002'):  # P2002 = Twitter Name
                                fWrite.write(line)
                                i += 1
                                print(i)
                        except json.decoder.JSONDecodeError:
                            continue
                fWrite.write("]\n")

            print("Written " + str(i) + " records to " + ModWikiDumpPath)
        else:
            print("File " + ModWikiDumpPath + " already exists")

This step could take over 24 hours to execute. It results in a much more manageable file. File is TwitterRelatedRecords.json and is 5.3 GB.

Step 2a:
There are 9,288 Wikidata properties. We utilize SPARQLQueryDirectly.py method getAllPropertiesFile() in order to get all of the properties, with code shown below:

    folderOut = 'Wiki/'

    df_record_all = pd.DataFrame(
        columns=['property', 'propertyLabel', 'propertyDescription', 'altLabel_list'])

    query =  '''
    SELECT ?property ?propertyLabel ?propertyDescription (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {
        ?property a wikibase:Property .
        OPTIONAL { ?property skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "en") }
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" .}
    }
    GROUP BY ?property ?propertyLabel ?propertyDescription
    '''
    data = executeWikiQuery(query)

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
    
We utilize SPARQLQueryDirectly.py method getPropertyUsagePerTwitterUser() in order to focus on most popular Wikidata properties for pages that have a social media Twitter account. An Excel spreadsheet is generated that contains the property, property English description, how many Twitter users contained the property. Here is a snapshot of top properties:
![image](https://user-images.githubusercontent.com/80060152/148464723-f68e9441-a1d3-40b6-9439-476360abdf2e.png)

Step 2b: We went through the first ~400 most popular properties and record those of interest in WikiDataPropertiesOfInterest.py
The properties that were found useful are recorded in MongoDB (the same exercise can be performed for other Social media or other Wikidata pages with reader having to filter out properties that would be useful for their application). On linux we create a separate folder that will contain MongoDB files and call this command from terminal to setup an instance of MongoDB on port 27020: sudo mongod --port 27020 --dbpath "/media/aleksei1985/Seagate Expansion Drive/MongoDBWikiData/" (reader should have MongoDB running on 27020 pointing to their instance).

Here is a snapshot of this MongoDB table being explored using MongoDB compass:
![image](https://user-images.githubusercontent.com/80060152/149199336-62d252fd-fd4a-471b-a255-51f52820694a.png)

Of particular interest is the Twitter_Screen_Name field.

Step 3: For all Twitter user screenanmes extracted (using Twitter_Screen_Name) the Twitter API is used to obtain recent up to date information on number of followers, Twitter user description, and other information. Here is a snapshot of this MongoDB table being explored using MongoDB compass. Some of the screennames may not be accurate or may be redundant across multiple wikidata pages (out of 308,365 Wikipages that mention a Twitter screenname, 284,105 are unique):
![image](https://user-images.githubusercontent.com/80060152/149199566-c79c576b-e0c5-4f18-aac8-cafa19e1d8da.png)

Step 4: Having identified all of the Wikidata pages that contain a Twitter screenanme and having verified that the screenanme exists using the Twitter API, we now want to explore all of the QNodes that each user is connected to (call the QNode1). We first go through the MongoDB database and record all unique QNode1

        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnUsers"
        Qnodes = collectQNodes(port, db_name, collectionName)

This routine finds 171,779 QNode1; we go through the original json.bz2 WikiData dump and keep all of the entries that contain one of these QNode1. 

        ModWikiDumpPath = '/home/aleksei1985/Desktop/WikiFiles/Qnodes.json'
        getRecordsRelatedToQNodesOfInterestJSON(Qnodes, ModWikiDumpPath)
        
This data is written to MongoDB to table WikiDataInfoOnQNodes.

        collectionName = "WikiDataInfoOnQNodes"
        processWikiDump(ModWikiDumpPath, port, db_name, collectionName, includeTwitterScreenName=False)

These steps are repeated a second time. In the second pass we are recording all of the Q nodes that are connected to QNode1 (call this Qnode2).

        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnQNodes"
        Qnodes = collectQNodes(port, db_name, collectionName)
        ModWikiDumpPath = '/home/aleksei1985/Desktop/WikiFiles/Qnodes2.json'
        getRecordsRelatedToQNodesOfInterestJSON(Qnodes, ModWikiDumpPath)
        collectionName = "WikiDataInfoOnQNodes2"
        processWikiDump(ModWikiDumpPath, port, db_name, collectionName, includeTwitterScreenName=False)

In a way what has occured is we have Wikipages referencing Twitter screenname -> these are connected to QNode1 Wikipages -> these are connected to QNode2 Wikipages. 

Step 5: For each QNode record the corresponding country association (working of the "P17" relation that specifies country).

        import pickle
        QnodeToCountry = {}
        collectionName = "WikiDataInfoOnQNodes"
        QnodeToCountry = generateNodeToCountry(port, db_name, collectionName, QnodeToCountry)
        collectionName = "WikiDataInfoOnQNodes2"
        QnodeToCountry = generateNodeToCountry(port, db_name, collectionName, QnodeToCountry)
        with open('QnodeToCountry.pickle', 'wb') as handle:
            pickle.dump(QnodeToCountry, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
Next for every QNode that the Twitter user is associated with we record all of the countries. For each user we are using the country that each user has the most relations to. For example if user j is (i) educated at USA, (ii) has country citizenship USA, and (iii) born in Brazil then the user j has connection to {USA: 2, BRA: 1} and so USA being the most frequent is the country assigned. We utilize this type of country association to compare against country data obtained via SocialBakers.

        collectionNameRead = "WikiDataInfoOnUsers"
        userToCountryAssociations = analyzeLocationDataCountry(port, db_name, collectionNameRead, QnodeToLabel, QnodeToCountry, QnodeToCountryISO)
        userToCountryTop = {}
        for user in userToCountryAssociations:
            d = userToCountryAssociations[user]
            if len(d) > 0:
                topCountry = sorted(d.items(), key=lambda x: x[1], reverse=True)[0][0]
                userToCountryTop[user] = topCountry
         
SocialBakers is a commercial website which provides top 100 Twitter user accounts for many countries around the world. These accounts were scrapped off the site. There is no info on how SocialBakers comes up with its methodology.

![image](https://user-images.githubusercontent.com/80060152/152063263-1b0a3a1c-fa4d-400c-81b1-79fa6b94029c.png)

On SocialBakers more well known accounts are listed like celebrities, major news, and others for which a Wikipedia page is likely to exist. As a result across the 13,574 users listed on SocialBakers 4,536 can be found on Wikidata or (25%). Of these users the country from Wikidata matches in 88.64% of cases. Advantage in WikiData is it goes beyond country data and in many cases lists city as well as a lot of other information. From preliminary review we find that for SocialBakers born in seems to be the predominant feature i.e. even though person educated in, lives in, and works in USA they will be associated with Russia if that is where they were born. This whole page was just a simple case of how a WikiData dump can be utilized to gain additional data and hopefully the reader can utilize bits of code for their own projects.
