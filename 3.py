import requests
import json

def extract():
    f = open("tmdb.json")
    if f:
        return json.loads(f.read())

def reindex(analysisSettings={}, mappingSettings={}, movieDict={}):
    settings = { #A
        "settings": {
            "number_of_shards": 1, #B
            "index": {
                "analysis" : analysisSettings, #C
            }}}

    if mappingSettings:
        settings['mappings'] = mappingSettings #C

    resp = requests.delete("http://localhost:9200/tmdb") #D
    resp = requests.put("http://localhost:9200/tmdb", 
                        data=json.dumps(settings))

    bulkMovies = ""
    print("building...")
    for id, movie in movieDict.iteritems(): 
        addCmd = {"index": {"_index": "tmdb", #E
                            "_type": "movie",
                            "_id": movie["id"]}}
        bulkMovies += json.dumps(addCmd) + "\n" + json.dumps(movie) + "\n"

    print("indexing...")
    resp = requests.post("http://localhost:9200/_bulk", data=bulkMovies)

if __name__ == "__main__":
    print("main")
