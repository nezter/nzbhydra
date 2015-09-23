import calendar
import datetime
import email
import logging
import time

from furl import furl

from datestuff import now
from nzb_search_result import NzbSearchResult
from search_module import SearchModule
logger = logging.getLogger('root')


def get_age_from_pubdate(pubdate):
    timepub = datetime.datetime.fromtimestamp(email.utils.mktime_tz(email.utils.parsedate_tz(pubdate)))
    timenow = now()
    dt = timenow - timepub
    epoch = calendar.timegm(time.gmtime(email.utils.mktime_tz(email.utils.parsedate_tz(pubdate))))
    pubdate_utc = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(email.utils.mktime_tz(email.utils.parsedate_tz(pubdate))))
    age_days = int(dt.days)
    return epoch, pubdate_utc, int(age_days)


class NewzNab(SearchModule):
    # TODO init of config which is dynmic with its path

    def __init__(self, config_section):
        super(NewzNab, self).__init__(config_section)
        self.module_name = "NewzNab"
        self.name = config_section.get("name")
        self.query_url = config_section.get("query_url")
        self.base_url = config_section.get("base_url")
        self.apikey = config_section.get("apikey")
        self.username = config_section.get("username")
        self.password = config_section.get("password")
        self.search_types = config_section.get("search_types", ["general", "tv", "movie"])
        self.supports_queries = config_section.get("supports_queries", True)
        self.search_ids = config_section.get("search_ids", ["tvdbid", "rid", "imdbid"])

    def build_base_url(self, action):
        url = furl(self.query_url).add({"apikey": self.apikey, "o": "json", "extended": 1, "t": action})
        return url

    def get_search_urls(self, query, categories=None):
        f = self.build_base_url("search").add({"q": query})
        if categories is not None:
            f.add({"cat": ",".join(str(x) for x in categories)})
        return [f.url]

    def get_showsearch_urls(self, query=None, identifier_key=None, identifier_value=None, season=None, episode=None, categories=None):
        if query is None:
            url = self.build_base_url("tvsearch")
            if identifier_key is not None:
                url.add({identifier_key: identifier_value})
            if episode is not None:
                url.add({"ep": episode})
            if season is not None:
                url.add({"season": season})
        else:
            url = self.build_base_url("search").add({"q": query})
        
        if categories is None:
            categories = [5000]
        
        url.add({"cat": ",".join(str(x) for x in categories)})
            
        
        return [url.url]

    def get_moviesearch_urls(self, query=None, identifier_key=None, identifier_value=None, categories=None):
        if query is None:
            url = self.build_base_url("movie")
            if identifier_key is not None:
                url.add({identifier_key: identifier_value})
        else:
            url = self.build_base_url("search").add({"q": query})
        
        if categories is None:
            categories = [2000]
        
        url.add({"cat": ",".join(str(x) for x in categories)})
        
        return [url.url]

    def process_query_result(self, json_response):
        import json
        # from Helpers import getAgeFromPubdate
        # from Helpers import sizeof_readable

        entries = []
        json_result = json.loads(json_response)
        if "0" == json_result["channel"]["response"]["@attributes"]["total"]:
            return entries

        result_items = json_result["channel"]["item"]
        if "title" in result_items:
            # Only one item, put it in a list so the for-loop works
            result_items = [result_items]
        for item in result_items:
            entry = NzbSearchResult()
            entry.title = item["title"]
            entry.link = item["link"]
            entry.pubDate = item["pubDate"]
            entry.epoch, entry.pubdate_utc, entry.age_days = get_age_from_pubdate(item["pubDate"])
            entry.precise_date = True
            entry.provider = self.name
            entry.attributes = []

            entry.categories = []
            for i in item["attr"]:
                if i["@attributes"]["name"] == "size":
                    entry.size = int(i["@attributes"]["value"])
                    # entry.sizeReadable = sizeof_readable(entry.size)
                elif i["@attributes"]["name"] == "guid":
                    entry.guid = i["@attributes"]["value"]
                elif i["@attributes"]["name"] == "category":
                    entry.categories.append(int(i["@attributes"]["value"]))
                # Store all the extra attributes, we will return them later for external apis
                entry.attributes.append({"name": i["@attributes"]["name"], "value": i["@attributes"]["value"]})
            entry.categories = sorted(entry.categories) #Sort to make the general category appear first
            entries.append(entry)
        return entries


def get_instance(config_section):
    return NewzNab(config_section)
