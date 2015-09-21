from pprint import pprint
import unittest

from searchmodules.newznab import NewzNab


class MyTestCase(unittest.TestCase):
    from config import cfg
    
    cfg["search_providers"]["1"]["search_module"] = "newznab"
    cfg["search_providers"]["1"]["name"] = "NZBs.org"
    cfg["search_providers"]["1"]["apikey"] = "apikeynzbsorg"
    cfg["search_providers"]["1"]["base_url"] = "https://nzbs.org"
    cfg["search_providers"]["1"]["query_url"] = "http://127.0.0.1:5001/nzbsorg"
    
    def testParseJsonToNzbSearchResult(self):
        from config import cfg
        n = NewzNab(cfg)
        
        #nzbsorg
        with open("tests/mock/nzbsorg_q_avengers_3results.json") as f:
            entries = n.process_query_result(f.read())
        pprint(entries)
        assert len(entries) == 3
        
        assert entries[0].title == "Avengers.Age.Of.Ultron.2015.FRENCH.720p.BluRay.x264-Goatlove"
        assert entries[0].size == 6719733587
        assert entries[0].guid == "9c9d30fa2767e05ffd387db52d318ad7"
        
        assert entries[1].title == "Avengers.Age.of.Ultron.2015.1080p.BluRay.x264.AC3.5.1-BUYMORE"
        assert entries[1].size == 4910931143
        assert entries[1].guid == "eb74f6c0bf2125c0b410936276ac38f0"
        
        assert entries[2].title == "Avengers.Age.of.Ultron.2015.1080p.BluRay.DTS.x264-CyTSuNee"
        assert entries[2].size == 15010196044
        assert entries[2].guid == "41b305ac99507f70ed6a10e45177065c"
        
        
        #dognzb
        with open("tests/mock/dognzb_q_avengers_3results.json") as f:
            entries = n.process_query_result(f.read())
        pprint(entries)
        assert len(entries) == 3
        
        assert entries[0].title == "Avengers.Age.Of.Ultron.2015.FRENCH.720p.BluRay.x264-Goatlove"
        assert entries[0].size == 6718866639
        assert entries[0].guid == "c6214fe5ae317b36906f0507042ca889"
        
        assert entries[1].title == "Avengers.Age.Of.Ultron.2015.1080p.BluRay.Hevc.X265.DTS-SANTI"
        assert entries[1].size == 5674463318
        assert entries[1].guid == "0199594cb9af69efb663e761848a76c2"
        
        assert entries[2].title == "Avengers.Age.Of.Ultron.2015.Truefrench.720p.BluRay.x264-AVITECH"
        assert entries[2].size == 6340781948
        assert entries[2].guid == "ea1b68d2ff97a5f0528b3d22c73f11ad"
        
    
    def testNewznabSearchQueries(self):
        
        nzbsorg = NewzNab(self.cfg.section("search_providers").section("1"))
        
        queries = nzbsorg.get_search_urls("aquery")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=search" in query
        assert "q=aquery" in query
        assert "o=json" in query
        
        queries = nzbsorg.get_showsearch_urls()
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=tvsearch" in query
        assert "o=json" in query
        
        queries = nzbsorg.get_showsearch_urls(categories="5432")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=tvsearch" in query
        assert "cat=5432" in query
        assert "o=json" in query
        
        queries = nzbsorg.get_showsearch_urls("8511")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=tvsearch" in query
        assert "rid=8511" in query
        assert "o=json" in query
        
        queries = nzbsorg.get_showsearch_urls("8511", "1")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=tvsearch" in query
        assert "rid=8511" in query
        assert "o=json" in query
        assert "season=1" in query
        
        queries = nzbsorg.get_showsearch_urls("8511", "1", "2")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=tvsearch" in query
        assert "rid=8511" in query
        assert "o=json" in query
        assert "season=1" in query
        assert "ep=2" in query
        
        queries = nzbsorg.get_moviesearch_urls("12345678")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=movie" in query
        assert "imdbid=12345678" in query
        assert "o=json" in query
        
        queries = nzbsorg.get_moviesearch_urls("12345678", "5432")
        assert len(queries) == 1
        query = queries[0]
        assert "http://127.0.0.1:5001/nzbsorg?" in query
        assert "apikey=apikeynzbsorg" in query
        assert "t=movie" in query
        assert "imdbid=12345678" in query
        assert "o=json" in query
        assert "cat=5432" in query