# WikiData

Download the latest WikiData dump as a .json.bz2 file from:
https://dumps.wikimedia.org/wikidatawiki/entities/
This is a 72 GB file as of Jan 6 2022.

Step 1:
Go through bz2 file line by line and see if a Twitter person is mentioned:

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

The reason we are focussing on Twitter is because it is the most popular. See file SPARQLQueryDirectly.py function recordSocialSiteInfo:
All of the Wikidata Property IDs can be found via query: query ?x wdt:P31 wd:Q105388954
![image](https://user-images.githubusercontent.com/80060152/148462393-55e0a641-3771-43eb-bed1-810373489f15.png)!

