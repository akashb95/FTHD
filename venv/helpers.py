import requests
from key import api_key

MAX_RESULTS = 100                       # default number of results on page

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


def lookup(query, offset=None, max_results=None):
    """
    Looks up query articles from FT using FT Headlines API.
    :param query: query string
    :param offset: (pageNumber - 1) * max_results
    :param max_results: number of results on page
    :return: list of articles with headlines, link to article, timestamp and a summary.
    """

    # check cache for articles
    if query in lookup.cache:
        # check if cache contains articles for the right page number and the right number of results
        if lookup.cache[query][-1]["offset"] == offset and lookup.cache[query][-1]["maxResults"] == max_results:
            return lookup.cache[query][:-1]

    # user-defined number of results per page
    if max_results:
        parameters["resultContext"]["maxResults"] = max_results

    # offset as defined by FT API - which index of articles to begin showing results from
    if offset:
        parameters["resultContext"]["offset"] = offset

    # user-entered query string
    parameters['queryString'] = query
    response = requests.post(endpoint, params=api, headers=headers, json=parameters).json()

    print(response)

    # number of articles found
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
    lookup.cache[query].append({'maxResults': max_results, 'offset': offset})

    # send everything but the result details
    return lookup.cache[query][:-1]


# initialize cache
lookup.cache = {}
