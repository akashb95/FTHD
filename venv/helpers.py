import requests
from key import api_key

MAX_RESULTS = 100

api = {"apiKey": api_key}

request_body = {"queryString": "",
                "queryContext": {"curations": ["ARTICLES", "PAGES"]},
                "resultContext": {"aspects": ["title", "lifecycle", "location", "summary", "editorial"]
                                  }
                }

headers = {"X-Api-Key": "59cbaf20e3e06d3565778e7b112bc62477c2437cb8ef99ce17384c44",
           "Content-Type": "application/json"}

parameters = {"queryString": "",
              "queryContext": {
                  "curations": ["ARTICLES", "PAGES"]
              },
              "resultContext": {
                  "aspects": ["title", "lifecycle", "location", "summary", "editorial"],
                  "maxResults": MAX_RESULTS,
                  "offset": 0,
                  "contextual": False,
                  "highlight": False,
                  "suppressDefaultSort": False
              }}

endpoint = "http://api.ft.com/content/search/v1?apiKey={}".format(api_key)


def lookup(query):
    """Looks up query articles."""

    # check cache for geo
    if query in lookup.cache:
        return lookup.cache[query]

    parameters['queryString'] = query
    response = requests.post(endpoint, params=api, headers=headers, json=parameters).json()

    index_count = response["results"][0]["indexCount"]
    try:
        articles = response["results"][0]["results"]

        # cache results
        lookup.cache[query] = [
            {"link": item["location"]["uri"], "title": item["title"]["title"], "summary": item["summary"],
             "timestamp": item["lifecycle"]["lastPublishDateTime"]}
            for item in articles]

    # if no results found
    except KeyError:
        lookup.cache[query] = None

    lookup.cache[query].append(index_count)

    return lookup.cache[query]


# initialize cache
lookup.cache = {}
