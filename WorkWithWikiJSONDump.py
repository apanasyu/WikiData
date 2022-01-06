import bz2
import json
import pandas as pd
import pydash

#WikiOriginalFilepath = '/media/aleksei1985/Seagate Expansion Drive/WikiKGTK/latest-all.json.bz2'
WikiOriginalFilepath = '/home/aleksei1985/Downloads/latest-all.json.bz2'
def getRecordsRelatedToTwitterUsersJSON(ModWikiDumpPath):
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

def readInAllTwitterScreenNames(port, db_name, collectionName):
    from MongoDBInterface import getMongoClient
    client = getMongoClient(port)
    db = client[db_name]
    collectionToRead = db[collectionName]

    tweetCursor = collectionToRead.find({}, no_cursor_timeout=True)
    TwitterScreenNames = set([])
    for nodeDict in tweetCursor:
        TwitterScreenNames.add(nodeDict["Twitter_Screen_Name"])

    print("Twitter screen names = " + str(len(TwitterScreenNames)))
    return TwitterScreenNames

def getRecordsRelatedToQNodesOfInterestJSON(Qnodes, ModWikiDumpPath):
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

                        if record["id"] in Qnodes:
                            fWrite.write(line)
                            i += 1
                            print(i)
                    except json.decoder.JSONDecodeError:
                        continue
            fWrite.write("]\n")

        print("Written " + str(i) + " records to " + ModWikiDumpPath)
    else:
        print("File " + ModWikiDumpPath + " already exists")

def readInTwitterRecords(ModWikiDumpPath):
    import json
    with open(ModWikiDumpPath, 'r') as f:
        for line in f:
            try:
                yield json.loads(line.rstrip(',\n'))
            except json.decoder.JSONDecodeError:
                continue

def collectQNodes(port, db_name, collectionName):
    from MongoDBInterface import getMongoClient
    client = getMongoClient(port)
    db = client[db_name]
    collectionToRead = db[collectionName]

    tweetCursor = collectionToRead.find({}, no_cursor_timeout=True)
    qNodes = set()
    for nodeDict in tweetCursor:
        for key in nodeDict:
            if key.startswith("P"):
                #print(json.loads(nodeDict[key]))
                Qnodes = nodeDict[key][1: -1].split(', ')
                Qnodes = set(Qnodes)
                for Qnode in Qnodes:
                    Qnode = Qnode[1: -1]
                    if Qnode.startswith("Q"):
                        qNodes.add(Qnode)

    print("Q nodes " + str(len(qNodes)))
    return qNodes

def processWikiDump(ModWikiDumpPath, port, db_name, collectionName, includeTwitterScreenName):
    from MongoDBInterface import getMongoClient
    client = getMongoClient(port)
    db = client[db_name]
    collectionToWrite = db[collectionName]

    from datetime import datetime
    totalWritten = 0
    userInfoToStore = []
    for record in readInTwitterRecords(ModWikiDumpPath):
        userInfoFromWikiData = {}

        userInfoFromWikiData["_id"] = record["id"]
        userInfoFromWikiData["wikiData_ID"] = record["id"]
        userInfoFromWikiData["english_label"] = pydash.get(record, 'labels.en.value')
        userInfoFromWikiData["english_desc"] = str(pydash.get(record, 'descriptions.en.value'))
        userInfoFromWikiData["num_sitelinks"] = len(record["sitelinks"])
        if includeTwitterScreenName:
            userInfoFromWikiData["Twitter_Screen_Name"] = pydash.get(record, 'claims.P2002[0].mainsnak.datavalue.value')

        coordinates = ""
        if pydash.has(record, 'claims.P625'):  # location
            latitude = str(pydash.get(record, 'claims.P625[0].mainsnak.datavalue.value.latitude'))
            longitude = str(pydash.get(record, 'claims.P625[0].mainsnak.datavalue.value.longitude'))
            coordinates = "(" + latitude + ", " + longitude + ")"
            userInfoFromWikiData["P625"] = coordinates

        from WikiDataPropertiesOfInterest import getPropertiesWikiData
        propertiesOfInterest = getPropertiesWikiData()
        for property in propertiesOfInterest:
            # example P31 property and possible values: Q5 = human, Q207694 = art museum, Q1549591 = big city, etc.
            if pydash.has(record, 'claims.' + str(property)):
                valuesOfType = []
                try:
                    if property in ["P856", "P1566", "P281", "P3134"]:
                        for types in record["claims"][str(property)]:
                            if types["mainsnak"]['snaktype'] == 'value':
                                valuesOfType.append(types["mainsnak"]["datavalue"]["value"])
                    elif property in ["P571", "P569", "P570"]:
                        for types in record["claims"][str(property)]:
                            if types["mainsnak"]['snaktype'] == 'value':
                                valuesOfType.append(types["mainsnak"]["datavalue"]["value"]["time"])
                    elif property == "P1705":
                        for types in record["claims"][str(property)]:
                            if types["mainsnak"]['snaktype'] == 'value':
                                valuesOfType.append(types["mainsnak"]["datavalue"]["value"]["language"])
                    elif property in ['P373', 'P973', 'P7859', 'P1581']:
                        for types in record["claims"][str(property)]:
                            if types["mainsnak"]['snaktype'] == 'value':
                                valuesOfType.append(types["mainsnak"]["datavalue"]["value"])
                    else:
                        valuesOfType = []
                        for types in record["claims"][str(property)]:
                            if types["mainsnak"]['snaktype'] == 'value':
                                valuesOfType.append(types["mainsnak"]["datavalue"]["value"]["id"])
                except:
                    print(property + " " + str(propertiesOfInterest[property]))
                    print(record["claims"][str(property)])

                types = str(valuesOfType)
                if "{" in types:
                    print(property + " " + str(propertiesOfInterest[property]))
                    print(record["claims"][str(property)])
                userInfoFromWikiData[str(property)] = types
                # print(property + " " + types)

        userInfoToStore.append(userInfoFromWikiData)

        if len(userInfoToStore) > 5000:
            try:
                collectionToWrite.insert_many(userInfoToStore, ordered=False)
                totalWritten += len(userInfoToStore)
                userInfoToStore = []
                print("SUCCESS written " + str(totalWritten) + " user info records to MongoDB " + str(datetime.now()))
            except Exception as e:
                print(e)

    if len(userInfoToStore) > 0:
        try:
            collectionToWrite.insert_many(userInfoToStore, ordered=False)
            totalWritten += len(userInfoToStore)
            userInfoToStore = []
            print("SUCCESS written " + str(totalWritten) + " user info records to MongoDB " + str(datetime.now()))
        except Exception as e:
            print(e)

def fillInDataUsingQNodes(port, db_name, collectionNameRead, collectionNameWrite, QnodeToLabel, QnodeToCoordinates):
    from WikiDataPropertiesOfInterest import getPropertyDescNoSpaces
    propertiesToEnglishLabel = getPropertyDescNoSpaces()

    from MongoDBInterface import getMongoClient
    client = getMongoClient(port)
    db = client[db_name]
    collectionToRead = db[collectionNameRead]
    collectionToWrite = db[collectionNameWrite]

    tweetCursor = collectionToRead.find({}, no_cursor_timeout=True)
    userInfoToStore = []
    from datetime import datetime
    totalWritten = 0
    for nodeDict in tweetCursor:
        nodeDict2 = {}
        for key in nodeDict:
            if key.startswith("P"):
                #print(json.loads(nodeDict[key]))
                Qnodes = nodeDict[key][1: -1].split(', ')
                Qnodes = set(Qnodes)
                QnodeValueFilledIn = []
                for Qnode in Qnodes:
                    Qnode = Qnode[1: -1]
                    if Qnode.startswith("Q"):
                        if Qnode in QnodeToCoordinates:
                            QnodeValueFilledIn.append(Qnode+"="+str(QnodeToLabel[Qnode])+"="+str(QnodeToCoordinates[Qnode]))
                        elif Qnode in QnodeToLabel:
                            QnodeValueFilledIn.append(Qnode+"="+str(QnodeToLabel[Qnode]))
                        else:
                            print(Qnode + " could not be found.")
                            QnodeValueFilledIn.append(Qnode)
                    else:
                        QnodeValueFilledIn.append(Qnode)
                if key == "P625":
                    nodeDict2[propertiesToEnglishLabel[key]] = nodeDict[key]
                else:
                    nodeDict2[propertiesToEnglishLabel[key]] = str(QnodeValueFilledIn)
            else:
                nodeDict2[key] = nodeDict[key]
        userInfoToStore.append(nodeDict2)

        if len(userInfoToStore) > 5000:
            try:
                collectionToWrite.insert_many(userInfoToStore, ordered=False)
                totalWritten += len(userInfoToStore)
                userInfoToStore = []
                print("SUCCESS written " + str(totalWritten) + " user info records to MongoDB " + str(datetime.now()))
            except Exception as e:
                print(e)

    if len(userInfoToStore) > 0:
        try:
            collectionToWrite.insert_many(userInfoToStore, ordered=False)
            totalWritten += len(userInfoToStore)
            userInfoToStore = []
            print("SUCCESS written " + str(totalWritten) + " user info records to MongoDB " + str(datetime.now()))
        except Exception as e:
            print(e)

def analyzeQNodes(port, db_name, collectionName, QnodeToLabel, QnodeToCoordinates):
    from MongoDBInterface import getMongoClient
    client = getMongoClient(port)
    db = client[db_name]
    collectionToRead = db[collectionName]

    tweetCursor = collectionToRead.find({}, no_cursor_timeout=True)
    for node in tweetCursor:
        QnodeToLabel[node["wikiData_ID"]] = node["english_label"]
        if "P625" in node:
            QnodeToCoordinates[node["wikiData_ID"]] = node["P625"]

    print(str(len(QnodeToLabel)) + " number of Q nodes")
    print(str(len(QnodeToCoordinates)) + " number of Q nodes with coordinates")
    return QnodeToLabel, QnodeToCoordinates

def analyzeLocationData(port, db_name, collectionNameRead, QnodeToLabel, QnodeToCoordinates):
    #from WikiDataPropertiesOfInterest import getPropertyDescNoSpaces
    #propertiesToEnglishLabel = getPropertyDescNoSpaces()

    from MongoDBInterface import getMongoClient
    client = getMongoClient(port)
    db = client[db_name]
    collectionToRead = db[collectionNameRead]

    userToCountry = {}
    usersWithCoordinates = set([])
    tweetCursor = collectionToRead.find({}, no_cursor_timeout=True)
    for nodeDict in tweetCursor:
        Qid = nodeDict["wikiData_ID"]

        for key in nodeDict:
            if key.startswith("P"):
                # print(json.loads(nodeDict[key]))
                Qnodes = nodeDict[key][1: -1].split(', ')
                Qnodes = set(Qnodes)
                QnodeValueFilledIn = []
                for Qnode in Qnodes:
                    Qnode = Qnode[1: -1]
                    if Qnode.startswith("Q"):
                        if Qnode in QnodeToCoordinates:
                            if not Qid in userToCountry:
                                userToCountry[Qid] = set([])
                            userToCountry[Qid].add(str(QnodeToLabel[Qnode]))
                if key == "P625":
                    usersWithCoordinates.add(Qid)

    print(len(usersWithCoordinates))
    print(len(userToCountry))
    print(len(set(userToCountry.keys()).intersection(usersWithCoordinates)))

    countryToCount = {}
    for user in userToCountry:
        for country in userToCountry[user]:
            if not country in countryToCount:
                countryToCount[country] = 0
            countryToCount[country] += 1

    import pandas as pd
    i = 0
    df_record_all = pd.DataFrame(columns=['id', 'count'])
    for country in countryToCount:
        df_record = pd.DataFrame({'id': country, 'count': countryToCount[country]},
                                 index=[i])
        df_record_all = df_record_all.append(df_record, ignore_index=True)
        i += 1

    folderOut = 'Wiki/'
    pd.DataFrame.to_csv(df_record_all, path_or_buf=folderOut + "analyzeLocationData.csv")
    print('CSV exported')

def getLocationInfoCityStateCountryZip(QnodeToCoordinates):
    qNodeToCityStateCountryZip = {}
    from geopy.geocoders import Nominatim

    # initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")

    for qnode in QnodeToCoordinates:
        print(QnodeToCoordinates[qnode])

    Latitude = "25.594095"
    Longitude = "85.137566"

    location = geolocator.reverse(Latitude + "," + Longitude)

    address = location.raw['address']

    # traverse the data
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')
    code = address.get('country_code')
    zipcode = address.get('postcode')
    print('City : ', city)
    print('State : ', state)
    print('Country : ', country)
    print('Zip Code : ', zipcode)

    with open('QnodeToCityStateCountryZip.pickle', 'wb') as handle:
        pickle.dump(QnodeToLabel, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':

    #step 1: since we are only interested in Twitter users, we do not need the whole Wikipedia dump, and so create a Wikipedia file with only Twitter user data
    print("Step 1")
    #ModWikiDumpPath = '/media/aleksei1985/Seagate Expansion Drive/WikiKGTK/TwitterRelatedRecords.json'
    ModWikiDumpPath = '/home/aleksei1985/Desktop/WikiFiles/TwitterRelatedRecords.json'
    getRecordsRelatedToTwitterUsersJSON(ModWikiDumpPath)

    port = 27020  # sudo mongod --port 27020 --dbpath "/media/aleksei1985/Seagate Expansion Drive/MongoDBWikiData2/"
    # step 2: collect fields of interest from Wikipedia and Twitter
    if False:
        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnUsers"
        processWikiDump(ModWikiDumpPath, port, db_name, collectionName, includeTwitterScreenName=True)
        TwitterUsers = readInAllTwitterScreenNames(port, db_name, collectionName)
        from GetTwitterUserInfo import main
        main(TwitterUsers, overWrite=False)

    # step 3: collect all Q nodes
    if True:
        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnUsers"
        Qnodes = collectQNodes(port, db_name, collectionName)
        #ModWikiDumpPath = '/media/aleksei1985/Seagate Expansion Drive/WikiKGTK/Qnodes.json'
        ModWikiDumpPath = '/home/aleksei1985/Desktop/WikiFiles/Qnodes.json'
        getRecordsRelatedToQNodesOfInterestJSON(Qnodes, ModWikiDumpPath)

        collectionName = "WikiDataInfoOnQNodes"
        processWikiDump(ModWikiDumpPath, port, db_name, collectionName, includeTwitterScreenName=False)

    # step 4: process Q node data second time
    if True:
        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnQNodes"
        Qnodes = collectQNodes(port, db_name, collectionName)
        #ModWikiDumpPath = '/media/aleksei1985/Seagate Expansion Drive/WikiKGTK/Qnodes2.json'
        ModWikiDumpPath = '/home/aleksei1985/Desktop/WikiFiles/Qnodes2.json'
        getRecordsRelatedToQNodesOfInterestJSON(Qnodes, ModWikiDumpPath)

        collectionName = "WikiDataInfoOnQNodes2"
        processWikiDump(ModWikiDumpPath, port, db_name, collectionName, includeTwitterScreenName=False)

    if True:
        #step 5 fill in as much info as possible using q nodes
        QnodeToLabel = {}
        QnodeToCoordinates = {}
        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnQNodes"
        QnodeToLabel, QnodeToCoordinates = analyzeQNodes(port, db_name, collectionName, QnodeToLabel, QnodeToCoordinates)
        #collectionName = "WikiDataInfoOnQNodes2"
        #QnodeToLabel, QnodeToCoordinates = analyzeQNodes(port, db_name, collectionName, QnodeToLabel, QnodeToCoordinates)

        db_name = "WikiDataTwitterUsers"
        collectionNameRead = "WikiDataInfoOnUsers"
        collectionNameWrite = "WikiDataInfoOnUsersQNodesFilledIn"
        #fillInDataUsingQNodes(port, db_name, collectionNameRead, collectionNameWrite, QnodeToLabel, QnodeToCoordinates)

    import os
    if not os.path.exists('QnodeToCoordinates.pickle'):
        QnodeToLabel = {}
        QnodeToCoordinates = {}
        db_name = "WikiDataTwitterUsers"
        collectionName = "WikiDataInfoOnQNodes"
        QnodeToLabel, QnodeToCoordinates = analyzeQNodes(port, db_name, collectionName, QnodeToLabel, QnodeToCoordinates)
        import pickle

        with open('QnodeToLabel.pickle', 'wb') as handle:
            pickle.dump(QnodeToLabel, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('QnodeToCoordinates.pickle', 'wb') as handle:
            pickle.dump(QnodeToCoordinates, handle, protocol=pickle.HIGHEST_PROTOCOL)

    QnodeToCoordinates = {}
    with open('QnodeToCoordinates.pickle', 'rb') as handle:
        QnodeToCoordinates = pickle.load(handle)
    #getLocationInfoCityStateCountryZip(QnodeToCoordinates)
    collectionNameRead = "WikiDataInfoOnUsers"
    #analyzeLocationData(port, db_name, collectionNameRead, QnodeToLabel, QnodeToCoordinates)
