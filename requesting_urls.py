import requests as req
import os.path
# https://en.wikipedia.org/wiki/Studio_Ghibli
# https://en.wikipedia.org/wiki/Star_Wars

# https://en.wikipedia.org/w/index.php
# - with parameters title=Main Page and action=info

def get_html ( url , params = None , output = None ):
    """ 
    This function makes a request for a url from a given website. It takes two optional
    parameters, one with parameters to get() function and other specifying if the response 
    is to be saved. It also creates requesting_urls folder if needed.
    Args: 
        url (String): a string representing url adress
        params (Dict): parameters to the get function
        output (String): file name of the file where result should be saved.
    Returns:
        response (String): html respons as string.
        if output is not null, than the result string is saved in the requesting_urls folder.    
    """
    # passing the optional paramters argument to the get function
    response = req.get( url , params = params )
    assert response.status_code == 200
    
    # if output is specified , the response txt and url get printed to a
    # txt file with the name in ‘output ‘
    if  output:
        
        directory = '.requesting_urls'
        filename = output
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        file.write(url)
        file.write(response.text)
        file.close()

    return response.text


html_str = get_html ("https://en.wikipedia.org/wiki/Studio_Ghibli", output =" output_Ghibli.txt")
html_str = get_html ("https://en.wikipedia.org/wiki/Star_Wars", output =" output_Star_Wars.txt")
html_str = get_html ( "https://en.wikipedia.org/w/index.php" , params ={"title": " Main page ", "action":"info"}, output =" output_main_page.txt")
