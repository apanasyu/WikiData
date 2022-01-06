def generateCSVFileWithUserInfo(collection, outputDir):
    tweetCursor = collection.find({}, no_cursor_timeout=True)

    fieldsOfInterest = ['screenName', 'followers_count', 'location', 'name', 'created_at', 'description']
    rows = [fieldsOfInterest]
    for userInfo in tweetCursor:
        row = []
        for field in fieldsOfInterest:
            row.append(userInfo[field])
        print(row)
        rows.append(row)

    writeRowsToCSV(rows, outputDir + collection.name + ".csv")

def writeRowsToCSV(rows, fileToWriteToCSV):
    import csv
    if len(rows) > 0:
        with open(fileToWriteToCSV, "w") as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(rows)
            fp.close()
            print("Written " + str(len(rows)) + " rows to: " + fileToWriteToCSV)

def main(WikiDataUserList, overWrite):
    outputDir = "Wiki/"
    from TwitterAPI import getAPI
    twitterAPI1 = getAPI()
    port = 27020
    #to start mongodb on new port do: sudo mongod --port 27020 --dbpath "/media/aleksei1985/Seagate Expansion Drive/MongoDBWikiData/"
    #wait for connection to be established can check using MongoDBCompass GUI that the database is ready to use
    step0 = True
    if step0:
        print("collecting info on Wikidata users")
        db_name = "WikiDataTwitterUsers"
        from MongoDBInterface import getMongoClient

        client = getMongoClient(port)
        from CollectUserInfo import mainProcessScreenNames
        db = client[db_name]

        collectionName = "WikiDataUsers"
        collectionToWrite = db[collectionName]

        if overWrite:
            collectionToWrite.drop()

        print(str(len(WikiDataUserList)) + " WikiDataUserList")

        mainProcessScreenNames(twitterAPI1, db_name, collectionName, WikiDataUserList, port, True)

        #generateCSVFileWithUserInfo(collectionToWrite, outputDir)

    '''
    step1 = False  # collect followers (see targeted user collection project for more info)
    if step1:
        influencers = WikiDataUserList
        #collect influencer's followers and profile information of each follower
        from MainDBSetup import setupDBUsingSingleUser

        maxFollowerToCollect = 500000
        for influencerScreenName in influencers:
            setupDBUsingSingleUser(twitterAPI1, influencerScreenName, maxFollowerToCollect, followersDir, port)
    '''