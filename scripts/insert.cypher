LOAD CSV WITH HEADERS FROM "file:///wiki.csv" AS csvLine
CREATE (p:Person {id: toInteger(csvLine.id), sourceName: csvLine.source_name, sourceUrl: csvLine.source_url, destName: csvLine.dest_name, destUrl: csvLine.dest_url})