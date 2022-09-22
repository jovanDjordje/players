import re
import os.path
from requesting_urls import get_html

def assemble_url(url, base_url=None):
    """
    Assembles an absolute url.

    Args: 
        url (String): url
        base_url (String): base url
    Returnes:
        url (String): assembled string    
    """
    https = "https:"

    if url.startswith("//"):
        return https+url
    if url.startswith("/") and  base_url:
        return base_url+url
    return url
    
def find_urls(html_string, base_url=None, out=None):
    """
    This function recieves a string of html and returnes a list of all urls found in the text.
    If out argument is not None, than a txt file with the reuslt urls is saved in the filter_urls folder.

    Args: 
        html_string (String): html string
        base_url (String): base url string
        out (String): output file name
    Returnes:
        return_list (List): list of all urls found.
        if out not None, than return:list data is stored in the appropriate folder.    
    """
    # YOUR CODE HERE
    # Remove duplicate urls
    # write list of urls to file if output not None
    # regex: matching <a characters then any char one to unlimeted (lazy).
    # regex cont: matching whitespace (0->unlim) finaly matching href, then whitespace (same as before)
    # regex cont: then match cahr = and whitespace after. Then match char ' or " zero and one times.
    # regex cont: them matching char not present here: " ' whitespace #. Finally match ' or " zero and one times.
    # the link to regex101: https://regex101.com/r/rQ8mR1/1 #https://regex101.com/r/ZAUhQd/1
    # test input: <a href ="#fragment-only">anchorlink</a>
    #             <a id ="some-id" href ="/relative/path#fragment">relative link</a>
    #             <a href ="//other.host/same-protocol">same-protocol link</a>
    #             <a href ="https://example.com"> absolute URL </a>
    link = re.compile("<a.+?\\s*href\\s*=\\s*[\"\\']?([^\"\\'\\s\\#>]+)[\"\\']?", flags=re.IGNORECASE)
      

    result_list = link.findall(html_string)
    no_duplicate = list(dict.fromkeys(result_list)) #list(set(result_list))
    return_list = [assemble_url(x, base_url) for x in no_duplicate]
    
     
    if  out:
        
        directory = '.filter_urls'
        filename = out
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        for item in return_list:
            file.write(item)
            file.write("\n")

        file.close()
    return return_list
# used for testing
html = """
<a href ="#fragment-only">anchorlink</a>
<a id ="some-id" href ="/relative/path#fragment">relative link</a>
<a href ="//other.host/same-protocol">same-protocol link</a>
<a href ="https://example.com"> absolute URL </a>
 """


def find_articles(html_string, output=None):
    """
    This function calls find_urls dunction and returnes only urls to Wikipedia articles.
    It also saves data to file if output argument is not None.

    Args:
        html_string (String): html string
        output (String): output file string
    """
    
    
    urls = find_urls(html_string, "https://en.wikipedia.org")
    
    # regex: here I tried some different solutions and found out that this one works even though it look a bit weird.
    # It is matching https:// and only word chars up until .wikipedia.org/wiki 
    # after which match lines without char :
    # regex 101 link: https://regex101.com/r/vfkkXN/1
    # test input is also provided through the link.
    # v2 i also tried and got a few more results in Nobel and Bundes
    # (.*\.wikipedia.org\/wiki[^:]+)$ here is the regex101 link https://regex101.com/r/tSZigw/1
    articles_regex = re.compile(r"(https:\/\/\w*\.wikipedia.org\/wiki[^:]+)$", flags=re.IGNORECASE)

 
    article_list=[articles_regex.findall(item) for item in urls if  articles_regex.findall(item)]
 
    if  output:
        
        directory = '.filter_urls'
        filename = output
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        for item in article_list:
            print("********** ")
            print(item[0])
            print("********** ")
            file.write(item[0])
            file.write("\n")

        file.close()

    return article_list
        




html_string_nobel = get_html("https://en.wikipedia.org/wiki/Nobel_Prize")
html_string_bundes = get_html("https://en.wikipedia.org/wiki/Bundesliga")
html_string_alp = get_html("https://en.wikipedia.org/wiki/2021–22_FIS_Alpine_Ski_World_Cup")

find_urls(html_string_nobel, "https://en.wikipedia.org", "nobel_final.txt")
find_urls(html_string_bundes, "https://en.wikipedia.org", "bundes_final.txt")
find_urls(html_string_alp, "https://en.wikipedia.org", "alp_final.txt")

find_articles(html_string_nobel, "nobel_prize_art_fin.txt")
find_articles(html_string_bundes, "bundes_art_fin.txt")
find_articles(html_string_alp, "alp_art_fin.txt")


test_str=["https://en.wikipedia.org/wiki/Regular_expression", "https://no.wikipedia.org/wiki/Regul%C3%A6rt_uttrykk",
    "https://hr.wikipedia.org/wiki/Srbija", "https://en.wikipedia.org/wiki/Agriculture",
    "https://en.wikipedia.org/wiki/History_of_the_domestic_sheep", "https://en.wikipedia.org/wiki/Gordon_Ramsay_Plane_Food",
    "https://www.w3schools.com/python/python_lists_comprehension.as",
    "https://en.wikipedia.org/wiki/Wikipedia:Good_articles/Agriculture,_food_and_drink",
    "https://en.wikipedia.org/wiki/Wikipedia:Disambiguation",
    "https://en.wikipedia.org/wiki/Wikipedia:Navigation_template","https://en.wikipedia.org/wiki/Avengers:_Endgame"]