# WikiData

Download the latest WikiData dump as a .json.bz2 file from:
https://dumps.wikimedia.org/wikidatawiki/entities/
This is a 72 GB file as of Jan 6 2022.

Step 1:
Go through bz2 file line by line and see if a Twitter person is mentioned 
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
