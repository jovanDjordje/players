from os import nice
from bs4 import BeautifulSoup
from requesting_urls import get_html
import re
import matplotlib.pyplot as plt
#from filter_urls import find_urls


def make_dict_list(lst, param):
    """
    Makes a list of dictionaries as specified in the precode {"name": name, param: param}
    Args:
        lst (list of lists): items in list contain name and param info
        param (String): statistic category
    Returnes:
        result (list of dictionaries): list of dictionaries to be ploted as precode defined     
    """
    result=[]
    d={}
    for item in lst:
        d["name"]=item[0]
        d[param]=item[1]
        result.append(d)
        d={}
    return result    

def select_first_three(dct, stat):
    """
    This function is sorting and returning a list with three best scores given the category
    Args:
        dct (Dict): dictionary with player statistics
        stat (String): category on which to sort (bpg, ppg, rpg)
    Returnes:
        Sorted list of three values.    
    """
    selector=0
    if stat=="bpg":
        selector=1
    if stat=="rpg":
        selector=2    
    
    #https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    s_ted = sorted(dct.items(), key=lambda x: float(x[1][selector]), reverse=True)
    result = []
    count=0
  
    for item in s_ted:
        if count>2:
            break
        result.append([item[0], item[1][selector]])
        count+=1

    return result

def nice_enum_print(items):
    """
    Prints elements and enumerates. Args is a list.
    """
    for count, value in enumerate(items):
        print(count, value)

def extract_teams ():
    """ Extract team names and urls from the NBA Playoff ’Bracket ’
    section table .
    
    Returns :
    team_names ( list ): A list of team names that made it to
    the conference
    semifinals .
    team_urls ( list ): A list of absolute Wikipedia urls
    corresponding to team_names .
    """
    # get html using for example get_html from requesting_urls
    html = get_html ( "https://en.wikipedia.org/wiki/2021_NBA_playoffs")
    # create soup
    soup = BeautifulSoup ( html , "html.parser")
    # find bracket we are interested in
    bracket_header = soup.find (id="Bracket")
    bracket_table = bracket_header.find_next ("table")
    rows = bracket_table.find_all ("tr")

    # create list of teams
    team_list = [] 
    team_urls=[]
    for i in range (1 , len ( rows )) :
        cells = rows[i].find_all("td")
        
        cells_text = [cell.get_text( strip = True ) for cell in cells ]  

        # filter out empty cells
        cells_text = [ cell for cell in cells_text if cell ]

        
        # Find the rows that contain seeding, team name and games won
        if len ( cells_text ) > 1:
            
            team_list.append(cells_text)
            team_link = rows[i].find('a')['href']
            team_urls.append("https://en.wikipedia.org"+team_link)
    # Filter out the teams that appear more than once , which means they made it
    # to the conference semifinals
    seen=[]
    seen_url=[]
    team_list_filtered =[]
    team_urls_filtered=[]
    # filtering team list
    for item in team_list:
        if not item[1] in seen:
            #print(item[1])
            seen.append(item[1])
        else:
            team_list_filtered.append(item[1])  
    # filtering urls
    for item in team_urls:
        if not item in seen_url:
            #print(item[1])
            seen_url.append(item)
        else:
            team_urls_filtered.append(item)          
    team_list_filtered = list(dict.fromkeys(team_list_filtered))# remove duplicates in order
    #nice_enum_print(team_list_filtered)         
  
    # create lists of team names and urls to the team website
    team_names = team_list_filtered
    team_urls = list(dict.fromkeys(team_urls_filtered)) # remove duplicates in order
    #nice_enum_print(team_urls)
    return team_names , team_urls 
 

tm_names, tm_links = extract_teams()

def extract_players ( team_url ):
    """ Extract players that played for a specific team in the NBA
    playoffs .

    Args :
    team_url ( str ): URL to the Wikipedia article of the season
    a given
    team .

    Returns :
    player_names ( list ): A list of players names corresponding to the team whos URL was passed .
    semifinals .
    player_urls ( list ): A list of Wikipedia URLs corresponding to
    player_names of the team whos URL was passed .

    """
    # keep base url
    base_url = "https://en.wikipedia.org"    
    # get html for each page using the team url you extracted before
    html = get_html ( team_url )
    # make soup
    soup = BeautifulSoup ( html , "html.parser")
    # get the header of the Roster
    roster_header = soup.find (id="Roster")
    # identify table
    roster_table = roster_header.find_next ("table")
    rows = roster_table.find_all ("tr")
    # prepare lists for player names and urls
    player_names = []
    player_urls = []
    # https://regex101.com/r/HOBSAw/1
    # positive lookahead, matches everything up until "("
    remove_parenthesis_reg = re.compile(r".*(?=\()", flags=re.IGNORECASE)
    for i in range (0 , len ( rows )) :
        cells = rows [i ].find_all("td")
        #print(cells)
        cells_text = [ cell.get_text ( strip = True ) for cell in cells ]

        if len ( cells_text ) == 7:
            rel_url = cells [2].find_next ("a").attrs ["href"]
            # Use e.g. regex to remove information in parenthesis following the name
            if(re.match(r".*(?=\()", cells_text[2])):
                player_names.append(remove_parenthesis_reg.findall(cells_text[2])[0])
            else:
                player_names.append(cells_text[2])    
            
        # create urls to each player
        # need to create absolute urls combining the base and the relative url
            player_urls.append ( base_url + rel_url )
      
    return player_names , player_urls
#https://en.wikipedia.org/wiki/2020%E2%80%9321_Milwaukee_Bucks_season
#extract_players("https://en.wikipedia.org/wiki/2020%E2%80%9321_Milwaukee_Bucks_season")


def extract_player_statistics ( player_url ) :
    """ Extract player statistics for NBA player .
    # Note : Make yourself familiar with the 2020 -2021 player statistics wikipedia page and adapt the code accordingly .

    Args :
    player_url ( str ): URL to the Wikipedia article of a player.

    Returns :
    ppg ( float ): Points per Game .
    bpg ( float ): Blocks per Game .
    rpg ( float ): Rebounds per Game .

    """
    # As some players have incomplete statistics / information , you can set a default score , if you want .
    ppg = 0.0
    bpg = 0.0
    rpg = 0.0

    # get html
    html = get_html ( player_url )

    # make soup
    soup = BeautifulSoup ( html , "html.parser")
    #print(type(soup))

    # find header of NBA career statistics
    nba_header = soup.find (id="NBA_career_statistics")

    # check for alternative name of header
    if nba_header is None :
        nba_header = soup.find (id="NBA")
    try:
    # find regular season header
    # You might want to check for different spellings , e.g.capitalization
    # You also want to take into account the different orders of header and table
        regular_season_header = nba_header . find_next (id="Regular_season")

    # next we should identify the table
        nba_table = regular_season_header . find_next ("table")
     
    except: 
        try :
            # table might be right after NBA career statistics header
            
            ploffs = nba_header.find_parent()
            ploffs2 = ploffs.find_next_sibling()
          
            if ploffs2.text.strip()=="Playoffs[edit]":# this is the case when there is no regular season table and it goes strait to playoffs
                return ppg , bpg , rpg
            else:
                nba_table = nba_header . find_next ("table")
                #print(nba_table)



        except :
            
            return ppg , bpg , rpg
    # find nba table header and extract rows
    table_header = nba_table.find_all ("th")
    #print("table header *********")
    rpg_column_idx=0
    bpg_column_idx=0
    ppg_column_idx=0


    for count, value in enumerate(table_header):
        #print(value.text.strip())
        if value.text.strip()=="RPG":
            #print(count, value)
            rpg_column_idx=count
        if  value.text.strip()=="BPG": 
            #print(count, value)
            bpg_column_idx=count 
        if  value.text.strip()=="PPG": 
            #print(count, value)
            ppg_column_idx=count 
  
    rows = nba_table.find_all ("tr") 
    for i in range (1 , len ( rows )) :
        cells = rows [i ].find_all("td")
        cells_text = [ cell.get_text ( strip = True ) for cell in cells ]
        
        # same as above, matching everything up until cross char
        remove_cross_reg=re.compile(r".*(?=\†)", flags=re.IGNORECASE)
        if(re.match(r".*(?=\†)", cells_text[0])):
                
                cells_text[0]= remove_cross_reg.findall(cells_text[0])[0]
                
        # as I was unable to match "en dash" with an ordinary dash I just removed it and inserted normal dash
        # this is probably not the best way to do it but it worked for me then and there.
        if len(cells_text[0])>4:
            first_part=cells_text[0][:4]
            last_part=cells_text[0][5:]
            cells_text[0]=first_part+"-"+last_part
        
        if(len(cells_text)==13):
            if(cells_text[0]=="2020-21" or  cells_text[0]=="2021"):
                if cells_text[rpg_column_idx]:
                    rpg=re.sub("\*", "", cells_text[rpg_column_idx])
                if cells_text[bpg_column_idx]:
                    bpg=re.sub("\*", "", cells_text[bpg_column_idx])
                if cells_text[ppg_column_idx]:
                    ppg=re.sub("\*", "", cells_text[ppg_column_idx])  
    scores=[rpg, bpg, ppg]
                 
    # Convert the scores extracted to floats
    # Note : In some cases the scores are not defined but only shown as ’- ’. In such cases you can just set the score to zero or not defined .
    for item in scores:
        try :
            item = float (item)
        except ValueError :
            item = 0.0
    # I left this print so that user knows what is going on, execution takes time...        
    print("S C O R E S ---------------------------+++++++++++++++++++")
    print(scores)
    print("S C O R E S ---------------------------++++++++++++++++++++")
    return scores[2] , scores[1] , scores[0]        

# links used for testing

# https://en.wikipedia.org/wiki/Elijah_Bryant

# https://en.wikipedia.org/wiki/Bryn_Forbes (NBA carrier stats)

# https://en.wikipedia.org/wiki/Axel_Toupane (no 2021)

# https://en.wikipedia.org/wiki/Jordan_Nwora (goes straight to playoffs)

# https://en.wikipedia.org/wiki/Jaden_Springer (does not have any relevant table)
# https://en.wikipedia.org/wiki/Grant_Riller (same)

# https://en.wikipedia.org/wiki/Joe_Ingles

#extract_player_statistics("https://en.wikipedia.org/wiki/Joe_Ingles")

def make_teams():
    """
    This function is producing three dictionaries. One for ppg, rpg and bpg.
    Key value in every dictionary is the team name while the value is the list of dictionaries.
    with name and stat value [{'name': Paul, 'ppg':2}]. See the "teams" variable for real example.
    Returnes:
        return_dict_ppg, return_dict_bpg, return_dict_rpg (Dict): described above
    """
    team_names, team_urls = extract_teams()
   
    return_dict_ppg={}
    return_dict_bpg={}
    return_dict_rpg={}
    for i in range(len(team_names)):
        players, player_url = extract_players(team_urls[i])
       
        player_stats = {}
        for y in range(len(players)):
            ppg, bpg, rpg = extract_player_statistics(player_url[y])
            arr = [ppg, bpg, rpg]
            player_stats[players[y]]= arr

        #print(player_stats) 
        three_best_ppg = select_first_three(player_stats, "ppg")
        #print(three_best) 
        return_dict_ppg[team_names[i]]=make_dict_list(three_best_ppg, "ppg")

        three_best_bpg = select_first_three(player_stats, "bpg")
        #print(three_best) 
        return_dict_bpg[team_names[i]]=make_dict_list(three_best_bpg, "bpg")

        three_best_rpg = select_first_three(player_stats, "rpg")
        #print(three_best) 
        return_dict_rpg[team_names[i]]=make_dict_list(three_best_rpg, "rpg")

  
    return return_dict_ppg, return_dict_bpg, return_dict_rpg     

     

        



teams_ppg, teams_bpg, teams_rpg = make_teams()

# example inner dictionary
d = {'Barton, Will': ['12.7', '.4', '4.0'], 'Bol, Bol': ['2.2', '.3', '.8'], 'Campazzo, Facundo': ['6.1', '.2', '2.1'], 
    'Čančar, Vlatko': ['2.1', '.0', '1.0'], 'Dozier, PJ': ['7.7', '.4', '3.6'], 
    'Gordon, Aaron': ['10.2', '.6', '4.7'], 'Green, JaMychal': ['8.1', '.4', '4.8'], 
    'Harrison, Shaquille': ['3.3', '.3', '2.3'], 'Howard, Markus': ['2.8', '.0', '.6'], 
    'Jokić, Nikola': ['26.4', '.7', '10.8'], 'McGee, JaVale': ['5.5', '1.1', '5.3'], 
    'Millsap, Paul': ['9.0', '.6', '4.7'], 'Morris, Monté': ['10.2', '.3', '2.0'], 
    'Murray, Jamal': ['21.2', '.3', '4.0'], 'Nnaji, Zeke': ['3.2', '.1', '1.5'], 
    'Porter, Michael': ['19.0', '.9', '7.3'], 'Rivers, Austin': ['8.7', '.1', '2.3']}


   

color_table = {
     "Philadelphia*" :"blue",
     "Atlanta*":"green",
     "Milwaukee*":"red",
     "Brooklyn": "yellow",
     "Utah*": "cyan",
     "LA Clippers": "orange",
     "Phoenix*":"violet",
     "Denver":"magenta"
 }

def plot_NBA_player_statistics ( teams, title, save, stat, aspect ) :
    """ Plot NBA player statistics. This code is from the precode mostly.
    Args: 
        teams (Dict): a dictionary with team names as keys and list of dictionary with name and stats as values
        title (String): plot title
        save (String): file name to save
        aspect (int): har coded value of y axis because a problem with overlaping the teams legend and bars. 
    """
    count_so_far = 0
    all_names = []
    plt.gcf().subplots_adjust(bottom=0.40)# prevent clipping of the player names
    #plt.axis('scaled')
    plt.ylim([0, int(aspect)])
    plt.rcParams['font.size'] = '8'
    # iterate through each team and the
    for team , players in teams.items() :
        # pick the color for the team , from the table above
        color = color_table [team]
        # collect the ppg and name of each player on the team
        # you ’ll want to repeat with other stats as well
        ppg = []
        names = []
        for player in players :
            names.append ( player ["name"])
            ppg.append ( float(player [stat]))
            #print(type(player["ppg"]))
            # record all the names , for use later in x label
        all_names.extend ( names )

        # the position of bars is shifted by the number of players so far
        x = range ( count_so_far , count_so_far + len( players ))
        count_so_far += len ( players )
        # make bars for this team ’s players ppg ,
        # with the team name as the label
        bars = plt.bar (x , ppg, color = color,  label = team ) # team
        # add the value as text on the bars
        plt.bar_label (bars, fontsize=6)
        

    # use the names , rotated 90 degrees as the labels for the bars
    plt.xticks ( range ( len ( all_names )) , all_names , rotation =90, fontsize=8)
    # add the legend with the colors for each team
    plt.legend ( loc="upper left", ncol = 3)
    # turn off gridlines
    plt.grid ( False )
    # set the title
    plt.title (title)
    # save the figure to a file
    plt.savefig (save)
    plt.clf()
    plt.cla()
    plt.close()  

# example how teams look like
teams = {'Philadelphia*': [{'name': 'Embiid, Joel', 'ppg': '28.5'}, {'name': 'Harris, Tobias', 'ppg': '19.5'}, {'name': 'Simmons, Ben', 'ppg': '14.3'}], 
'Atlanta*': [{'name': 'Young, Trae', 'ppg': '25.3'}, {'name': 'Collins, John', 'ppg': '17.6'}, {'name': 'Bogdanović, Bogdan', 'ppg': '16.4'}], 
'Milwaukee*': [{'name': 'Antetokounmpo, Giannis', 'ppg': '28.1'}, {'name': 'Middleton, Khris', 'ppg': '20.4'}, {'name': 'Holiday, Jrue', 'ppg': '17.7'}], 
'Brooklyn': [{'name': 'Durant, Kevin', 'ppg': '26.9'}, {'name': 'Irving, Kyrie', 'ppg': '26.9'}, {'name': 'Harden, James', 'ppg': '24.6'}], 
'Utah*': [{'name': 'Mitchell, Donovan', 'ppg': '26.4'}, {'name': 'Clarkson, Jordan', 'ppg': '18.4'}, {'name': 'Bogdanović, Bojan', 'ppg': '17.0'}], 
'LA Clippers': [{'name': 'Leonard, Kawhi', 'ppg': '24.8'}, {'name': 'George, Paul', 'ppg': '23.3'}, {'name': 'Morris, Marcus', 'ppg': '13.4'}], 
'Phoenix*': [{'name': 'Booker, Devin', 'ppg': '25.6'}, {'name': 'Paul, Chris', 'ppg': '16.4'}, {'name': 'Ayton, Deandre', 'ppg': '14.4'}], 
'Denver': [{'name': 'Jokić, Nikola', 'ppg': '26.4'}, {'name': 'Murray, Jamal', 'ppg': '21.2'}, {'name': 'Porter, Michael', 'ppg': '19.0'}]}

plot_NBA_player_statistics ( teams_ppg, "Points per game", "ppgV2.png", "ppg", 60 )      
plot_NBA_player_statistics ( teams_bpg, "Blocks per game", "bpgV2.png", "bpg" , 6)      
plot_NBA_player_statistics ( teams_rpg, "Rebounds per game", "rpgV2.png", "rpg", 30 )      

