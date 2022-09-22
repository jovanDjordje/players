import re
from bs4 import BeautifulSoup
from requesting_urls import get_html
import os

def extract_events ( url ):
    """ Extract date , venue and discipline for competitions .
    Your documentation here .
    Args :
       url (str): The url to extract events from .
    Returns :
       table_info ( list of lists ): A nested list where the rows represent each
       race date , and the columns are [date , venue , discipline ].
    """
    disciplines={
                 "DH": " Downhill ",
                 "SL": " Slalom ",
                 "GS": " Giant Slalom ",
                 "SG": " Super Giant Slalom ",
                 "AC": " Alpine Combined ",
                 "PG": " Parallel Giant Slalom ",
                 }
    #https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup
    html = get_html(url)
    soup = BeautifulSoup (html,"html.parser")
    calendar_header = soup.find(id="Calendar")

    calendar_table = calendar_header.find_all_next("table")[0]

    rows = calendar_table.find_all("tr")

    found_event = None
    found_venue = None
    found_discipline = None

    events = []
    full_row_length = 11
    short_row_length = full_row_length - 2
    intermediate_row_length = full_row_length - 1
    for row in rows :
        cells = row.find_all("td")   
    
        if len ( cells ) not in { full_row_length , short_row_length, intermediate_row_length }:
            continue
            
        event = cells [2] 
        #print(cells[1])
        # this regex is just checking the overall form of the date in the table (digit(one or two)month()four digits as year)
        # this part: (\/|-|\s*)? is just checking / or - or whitespace between day-month
        # it is probably redundant but why not
        if re.match (r"(\d{1,2})(\/|-|\s*)?((January|February|March|April|May|June|July|August|September|October|November|December)|\d{2})(\/|-|\s*)?(\d{4})"
            , event.text.strip()):
            found_event = event.text.strip()
        else :
            found_event = None  
        if len ( cells ) == full_row_length:
            venue_cell = cells [3]
            found_venue = venue_cell.text.strip()
            discipline_index = 5 
        elif len ( cells ) == intermediate_row_length: # handling table entry with 10 columns 
             
             discipline_index = 4   
        else :
            discipline_index = 3
       
        discipline = cells [ discipline_index ] 
        # find the discipline id
        # can you make a regex to find only the keys of the disciplines dictionary ?
        # (DH |...) 
        discipline_regex = r"(DH |SL |GS |SG |AC |PG )"

        discipline_match = re.search(discipline_regex, discipline.text.strip()) 
        
        key=discipline.text.strip()[0]+discipline.text.strip()[1]
        
        if discipline_match :
        # look up the full discipline name
            found_discipline = disciplines.get(key)
        else :
            found_discipline = None
        if found_venue and found_event and found_discipline :
            events.append (( found_event , found_venue , found_discipline ))  
           

    return events                  


def create_betting_slip ( events , save_as ) :
    """
    Creates a betting slip. This function is from the precode provided.

    Args: 
        events (list of lists): nested list containing date, venue, discipline data [date, venue, disc]
        save_as (String): output file name                    

    """
   
    # ensure directory exists
    os.makedirs(" datetime_filter ", exist_ok = True )   
    with open ( f"./ datetime_filter /{ save_as }. md", "w") as out_file :
        out_file.write (f"# BETTING SLIP ({ save_as })\n\ nName :\n\n")
        out_file.write (" Date | Venue | Discipline | Who wins ?\n")
        out_file.write (" --- | --- | --- | --- \n")
        for e in events :
            date,venue , type = e
            out_file . write (f"{ date } | { venue } | { type } | \n")


#https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup
create_betting_slip(extract_events("https://en.wikipedia.org/wiki/2021%E2%80%9322_FIS_Alpine_Ski_World_Cup"), "table_events")            