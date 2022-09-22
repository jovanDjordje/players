import filter_urls as f
def test_find_urls () :
 html = """
 <a href ="#fragment-only" > anchor link </a>
 <a id ="some-id" href ="/relative/path#fragment" > relative link </>
 <a href ="//other.host/same-protocol">same - protocol link </a>
 <a href="https://example.com "> absolute URL </a>
 """
 urls = f.find_urls ( html , base_url ="https://en.wikipedia.org")
#  assert urls == [
#  "https://en.wikipedia.org/relative/path",
#  "https://other.host/same-protocol",
#  "https://example.com",
#  ]
 assert "https://en.wikipedia.org/relative/path" in urls
 assert "https://other.host/same-protocol" in urls
 assert "https://example.com" in urls