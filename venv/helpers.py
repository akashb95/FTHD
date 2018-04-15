import requests
from key import api_key

MAX_RESULTS = 50  # default number of results on page

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
                  "contextual": True,
                  "highlight": True,
                  "suppressDefaultSort": False
              }}

endpoint = "http://api.ft.com/content/search/v1?apiKey={}".format(api_key)


def lookup(query, offset, max_results=None):
    """

    Looks up query articles from FT using FT Headlines API.
    :param query: [str] query string
    :param offset: [int] (pageNumber - 1) * max_results
    :param max_results: [int] number of results on page
    :return: [List] list of articles with headlines, link to article, timestamp and a summary.
    """

    parsed_articles = {}

    if max_results:
        parameters["resultContext"]["maxResults"] = max_results

    parameters["resultContext"]["offset"] = offset

    parameters["queryString"] = query

    response = requests.post(endpoint, params=api, headers=headers, json=parameters).json()

    index_count = response["results"][0]["indexCount"]

    try:
        articles = response["results"][0]["results"]
        parsed_articles[query] = [{"link": item["location"]["uri"], "title": item["title"]["title"],
                                   "summary": item["summary"],
                                   "timestamp": parse_datetime(item["lifecycle"]["lastPublishDateTime"])}
                                  for item in articles]

    except KeyError:
        parsed_articles[query] = [None]

    parsed_articles[query].append(index_count)

    return parsed_articles[query]


def parse_datetime(dt):
    """
    Parses timestamp string received from API and makes it more readable.
    :param [str] dt: timestamp
    :return: [str] parsed timestamp
    """
    year = dt[:4]
    month = dt[5:7]
    day = dt[8:10]

    hour = dt[11:13]
    mins = dt[14:16]

    parsed = "{day}/{month}/{year} at {hour}:{mins}".format(day=day, month=month, year=year, hour=hour, mins=mins)

    return parsed
