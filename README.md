# Social Media Types
We are focussing on Twitter because it is the most popular. See file SPARQLQueryDirectly.py function recordSocialSiteInfo():
All of the Wikidata Property IDs can be found via query: query ?item wdt:P31 wd:Q105388954
![image](https://user-images.githubusercontent.com/80060152/148462393-55e0a641-3771-43eb-bed1-810373489f15.png)!

Here are the top 10 out of 64 most popular social media accounts to be listed (for query from November 2021):
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
As the table shows Twitter, Facebook, and Instagram are by far the most popular.

# Working with WikiData
Step 0: Download the latest WikiData dump as a .json.bz2 file from:
https://dumps.wikimedia.org/wikidatawiki/entities/
This is a 72 GB file as of Jan 6 2022.

Step 1: This step produces a file that now contains only WikiData pages that mention a Twitter user name. A lot of WikiData is related to stars, chemicals, and other info that is not relevant to our use case.

Go through downloaded bz2 file line by line and see if a Twitter person is mentioned (looking for P2002, if we wanted to focus on Facebook would use P2013, for Instagram P2003, and so on):

        with open(ModWikiDumpPath, 'w') as fWrite:
            with bz2.open(WikiOriginalFilepath, mode='rt') as fRead:
                firstTwoBytes = fRead.read(2)  # skip first two bytes: "[\n"
                fWrite.write(firstTwoBytes)
                for line in fRead:
                    try:
                        record = json.loads(line.rstrip(',\n'))
                        if pydash.has(record, 'claims.P2002'):  # P2002 = Twitter Name
                            fWrite.write(line)
                    except json.decoder.JSONDecodeError:
                        continue
            fWrite.write("]\n")


