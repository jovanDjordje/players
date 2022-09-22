from requesting_urls import get_html
import os.path
import re



def subs_mont_with_num(d_element, key):
    """
    This function is replacing the text month value with corresponding num value.
    Args:
        d_element (String): string with data about the date
        key (String): value to identify which month should be replaced.
    Retrnes:
        ret_elem (String): date element with number representing month    
    """
    ret_elem=""
    
    if key.lower().startswith("jan"):
        ret_elem=re.sub(r"[jJ]an(?:uary)?", "01", d_element)
    elif key.lower().startswith("feb"):  
        ret_elem=re.sub(r"[fF]eb(?:ruary)?", "02", d_element)
    elif key.lower().startswith("mar"):      
        ret_elem=re.sub(r"[mM]ar(?:ch)?", "03", d_element)  
    elif key.lower().startswith("apr"):
        ret_elem=re.sub(r"[aA]pr(?:il)?", "04", d_element)            
    elif key.lower().startswith("may"):    
        ret_elem=re.sub(r"[mM]ay", "05", d_element)
    elif key.lower().startswith("jun"):        
        ret_elem=re.sub(r"[jJ]un(?:e)?", "06", d_element)
    elif key.lower().startswith("jul"):
        ret_elem=re.sub(r"[jJ]ul(?:y)?", "07", d_element)              
    elif key.lower().startswith("aug"):    
        ret_elem=re.sub(r"[aA]ug(?:ust)?", "08", d_element)
    elif key.lower().startswith("sep"):    
        ret_elem=re.sub(r"[sS]ept(?:ember)?", "09", d_element)
    elif key.lower().startswith("oct"):
        ret_elem=re.sub(r"[oO]ct(?:ober)?", "10", d_element)      
    elif key.lower().startswith("nov"):    
        ret_elem=re.sub(r"[nN]ov(?:ember)?", "11", d_element)
    elif key.lower().startswith("dec"):
        ret_elem=re.sub(r"[dD]ec(?:ember)?", "12", d_element)
  
    return ret_elem



    
    
def find_dates(html_str, out=None):
    """
    Recieves html string and returnes a list of all dates
    The returned list is in format:
    - 1998/10/02
    - 1998/11/04

    Formats considered:
    DMY: 13 Oct(ober) 2020
    MDY: Oct(ober) 13, 2020
    YMD: 2020 Oct(ober) 13
    ISO: 2020-10-13
    """
    dec=r"\b[dD]ec(?:ember)?\b"
    jan=r"\b[jJ]an(?:uary)?\b"
    feb=r"\b[fF]eb(?:ruary)?\b"
    march=r"\b[mM]ar(?:ch)?\b"
    april=r"\b[aA]pr(?:il)?\b"
    may=r"\b[mM]ay\b"
    june=r"\b[jJ]un(?:e)?\b"
    july=r"\b[jJ]ul(?:y)?\b"
    aug=r"\b[aA]ug(?:ust)?\b"
    sept=r"\b[sS]ept(?:ember)?\b"
    oct=r"\b[oO]ct(?:ober)?\b"
    nov=r"\b[nN]ov(?:ember)?\b"
    # this regex is from the provided precode
    months = rf"(?:{jan}|{feb}|{march}|{april}|{may}|{june}|{july}|{aug}|{sept}|{oct}|{nov}|{dec})"
    # this regex should allow values 00-31 included only 0-1 values for days.
    day=rf"(?:[1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])"
    # regex is weird. Even though this regex seems wrong I've landed on it through
    # trial and error. It works as far as i was able to test it.
    # https://regex101.com/r/HAQvz2/1
    year=rf"(?:[19|20][0-9][0-9]{{2}})" # allowes years from 1900-2099
    #year_2= rf"(20[1-9][0-9])"

    # https://regex101.com/r/Ip3vfw/1
    dmy=rf"{day} {months} {year}" #\s{mon}\s{year}" // {year_2} // (\b[jJ]ul(?:y)?\b) worked last

    result=re.findall(rf"{dmy}", html_str)
   

    # general idea is to run through html_string and find dates dmy then rearange, add to return list
    # do the same with  mdy, ymd and iso
    return_list=[]
    # iterating through result list (dmy findall result)
    for elem in result:
         mth=re.findall(rf"{months}", elem) #getting the month
         num=re.findall (r"\d+ ", elem) # getting the day but also whitespace to the right of digit
         if len(num[0])==2: # if num[0] is longer then 2, meaning it has one digit and empty space.
            #print(num[0])
            l_zero_fix="0"+num[0]
            # in this branch we know that the day is one digit, therefor, adding leading zero
            t= re.sub(rf"{day} ", rf"{l_zero_fix}", elem)
            t= re.sub(rf"({day}) ({months}) ({year})", r"\3/\2/\1", t)# rearange
            t = subs_mont_with_num(t, mth[0])# get month as digit
            return_list.append(t) # add to return list
            #print(" ******* " + t)
         else:   
            #print(mth[0]+ "  --mth")
            # day is two digits so we rearange and get digit month
            date_element = re.sub(rf"({day}) ({months}) ({year})", r"\3/\2/\1", elem)
            #print(date_element)
            date_element_num=subs_mont_with_num(date_element, mth[0])
            #print(date_element_num + " -sub")
            return_list.append(date_element_num) # add to return list
       
    mdy= rf"{months} {day}\, {year}"  
    # even though one might argue here that i repeat a lot of code, let me conter that with the need
    # to slightly adjust regex here and there and thats why I choose to keep it like this cause i think it
    # gives me better overview. At least for now.
    result_mdy= re.findall(rf"{mdy}", html_str)
    #print(result_mdy)

    # repeating the same procedure as above
    for item in result_mdy:
        mth_mdy=re.findall(rf"{months}", item)
        date_element_mdy = re.sub(rf"({months}) ({day}\,) ({year})", r"\3/\1/\2", item)
        
        # I used forward and backward lookup here to get to day digits. So I tried to 
        # delimit with "/" on the left and "," on the right and tahe whats in-between.
        # https://regex101.com/r/SDJBR5/1
        # even though regex101 is matching more than meets the eye, it works as described.
        # unprint the print on line 139 and run test_collect_d() and the print for dates 
        # April 1, 2003. May 09, 2004. Jun 15, 2005 is -> 1 09 15.
        numb = re.findall(r"(?<=\/)(?:[1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1]).*(?=\,)", date_element_mdy)
        #print(numb[0])
        if(len(numb[0])==1):
            l_zero_fix_mdy="0"+numb[0]
            t_added_zero=re.sub(r"(?<=\/)(?:[1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1]).*(?=\,)", rf"{l_zero_fix_mdy}", date_element_mdy)
            t_sub_month=subs_mont_with_num(t_added_zero, mth_mdy[0])
            #print (t_sub_month + "T REPLACED LEAD ZERO/ SUB MONTH DONE")
            t_sub_month=re.sub(r"\,", "", t_sub_month) # getting rid of the comma
            return_list.append(t_sub_month)
        else:    
            date_element_mdy=subs_mont_with_num(date_element_mdy, mth_mdy[0])
            #print(date_element_mdy+" SUB MONTH")
            date_element_mdy=re.sub(r"\,", "", date_element_mdy)
            return_list.append(date_element_mdy)
        

    
    # changed day regex slightly because in some cases when the day was last, it wouldnt recognize number 29
    # should match 0 or 1, 0 or 1 times, 0 and 0-9, 1 and 1-9, 2 and 2-9 and 3 and 0-1
    # https://regex101.com/r/g99StB/1
    day_v2 = rf"(?:[01]?[0-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])\b"# should allow one digit days 0-9 00-31, very likely some duplicate regex here, but it worked
    ymd = rf"{year} {months} {day_v2}" 

    result_ymd= re.findall(rf"{ymd}", html_str)
    

    for ymd in result_ymd:
        #print(ymd)
        mth_ymd=re.findall(rf"{months}", ymd)
        num_ymd=re.findall (r" \d+", ymd)
        if(len(num_ymd[0])==2):
            # i have to remove white space before the number here
            l_zero_fix_ymd="0"+re.sub(r" ", r"", num_ymd[0]) # whitespace is befor digit, need to get rid of it
            
            t_ymd_add_l_z= re.sub(rf" {day}", rf" {l_zero_fix_ymd}", ymd)# adding leading zero
            
            t_rearange= re.sub(rf"({year}) ({months}) ({day})", r"\1/\2/\3", t_ymd_add_l_z) # rearanging
            
            t_sub_m_ymd=subs_mont_with_num(t_rearange, mth_ymd[0])
            
            return_list.append(t_sub_m_ymd)
        else:
            date_element_ymd= re.sub(rf"({year}) ({months}) ({day})", r"\1/\2/\3", ymd)
            date_element_ymd=subs_mont_with_num(date_element_ymd, mth_ymd[0])
            return_list.append(date_element_ymd)   

    
    iso_month = r"\b(?:0\d|1[0-2])\b" # this regex is from the precode

    iso=rf"{year}\-{iso_month}\-{day}\b" 
    result_iso= re.findall(rf"{iso}", html_str)

    
    for d in result_iso:
        # This regex is capturing only day digits (third group in rgex l->r)as it does not have ?:
        # https://regex101.com/r/och8cM/1
        num_iso=re.findall (r"(?:\d*)\-(?:\d*)\-(\d*)", d)
        #print("num_iso->"+num_iso[0]+"<-")
        if(len(num_iso[0])==1):
            l_z_fix_iso="0"+num_iso[0]
            
            # replacing the fixed leading zero and aranging at the same time
            t_rearange= re.sub(rf"({year})\-({iso_month})\-({day})", rf"\1/\2/{l_z_fix_iso}", d)

            #print(t_rearange + " ISO T REARANGE IN LEN=1")

            return_list.append(t_rearange)
        else:
            date_elem_iso = re.sub(rf"({year})\-({iso_month})\-({day})", r"\1/\2/\3", d) 
            return_list.append(date_elem_iso)

    
    if  out:
        
        directory = '.collect_dates_regex'
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


# testing strings with hidden dates
test_str_dmy = """Harry Potter and the Deathly Hallows</a></i>.<sup id="cite_ref-86" class="reference">
<a href="#cite_note-86">&#91;86&#93;</a></sup> In February 2007, it 
was reported that Rowling wrote on a bust in her hotel room at the 
<a href="/wiki/Balmoral_Hotel" title="Balmoral Hotel">Balmoral Hotel
</a> in Edinburgh that she had finished the seventh book in that 
room on 11 January 2007.<sup id="cite_ref-87" class="reference">
<a href="#cite_note-87">&#91;87&#93;</a></sup> <i>Harry Potter and the Deathly Hallows</i> 
was released on 21 July 2007 (0:01 <a href="/wiki/Western_European_Summer_Time" 
title="12 sept 2017Western 2 mar 2020European Summer 5 apr 2020Time">BST</a>)8 sept 2021<sup id="cite_ref-88" class="reference">
<a href="#cite_note-88">&#91;88&#93;</a></sup> and broke its predecessor's r
ecord as the fastest-selling book of all time.<sup id="cite_ref-sales_89-0" 
class="reference"> 07 mar 1982<a href="#cite_note-sales-89">&#91;89&#93;</a></sup>
It sold 11&#160;million copies in the first day of release in the United Kingdom 
and United States.<sup id="cite_ref-sales_89-1" class="reference">
<a href="#cite_note-sales-89">&#91;89&#93;</a>
</sup> The book's 7 may 1998last chapter was one of the earliest things she wrote in the entire series.<sup id="cite_ref-last_chapter_90-0" class="reference">
<a href="#cite_note-last_chapter-90">&#91;90&#93;</a></sup>"""

test_str_mdy_ymd_iso = """<li id="cite_note-252">Retrieved 2020-12-14.</span<span class="mw-cite-backlink"><b>
<a href="#cite_ref-252">^<2021 Nov 02/a></b></span> <span class="reference-text">
<link rel="mw-deduplicated-inline-style" 2020-11-12href="mw-data:TemplateStyles:r999302996"/>
<cite id="CITEREFPond2014" 1981 oct 3class="citation web cs1">Pond, Steve (February 21, 2014)
. <a rel mar 7, 1983="nofollow" 2019-08-13 class="external text" 
href="https://thewrap.com/john-lasseter-disney-fired-frozen-healed-studio-oscarwrap-down-wire">
"Why Disney Fired John Lasseter&#160;– And How He Came Back to Heal the Studio"</a>. 
<i><a href="/wiki/TheWrap" Dec 20, 1992title="TheWrap">TheWrap</a></i>. The Wrap News Inc. 
<a rel="nofollow" class="external 2018-14-14 text" 
href="https://web.archive.org/web/20140508200853/http://www.thewrap.com/john-lasseter-disney-fired-frozen-healed-studio-oscarwrap-down-wire">Archived</a> 
from the original on May 8, 2014<span class="reference-accessdate">. 
Retrieved <span class="nowrap">May 10,</span> 2014</span>.</cite>1982 march 07
<span title="ctx_ver=Z39.88-2004&amp;rft_val 2006 jan 29._fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;
1984 april 30. 1984 jun 5 1984 jul 11"""

test_iso_dates="""<li id="cite_note-252">Retrieved 2020-12-12.</span
<span2020-11-12<href="mw-data:TemplateStyles<a rel mar 7, 1983="nofollow" 2019-08-23 class="external text" 
href="https://thewrap.com/john-lasseter-disney-fired-frozen-healed-studio-oscarwrap-down-wire"><i><a href="/wiki/TheWrap" Dec 20, 1992title="TheWrap">TheWrap</a></i>. The Wrap News Inc. 
<a rel="nofollow"2025-09-9. class=2023-04-3"external 2018-14-14 text" 


"""

test_all="""on 1 Jan 2000. 10 february 2001. 29 mar 2002.
April 1, 2003. May 09, 2004. Jun 15, 2005< 2006 jul 3. 2007 aug 18.<: 2008 September 30
 2009-10-31, 2010-11-1, 2011-07-05"""


def test_collect_d ():
    """
    This function is testing if find_dates works. I couldnt use pytest because of
    some weird import error where it would not import requests. Even though it worked fine one week ago.
    I couldnt fix it so I made this function in order to have at least some sort of validation.
    """

    test_all="""on 1 Jan 2000. 10 february 2001. 29 mar 2002.
    April 1, 2003. May 09, 2004. Jun 15, 2005< 2006 jul 3. 2007 aug 18.<: 2008 September 30
    2009-10-31, 2010-11-1, 2011-07-05"""

    l = find_dates(test_all)
    assert l[0]=='2000/01/01' 
    assert l[1]=='2001/02/10' 
    assert l[2]=='2002/03/29' 
    assert l[3]=='2003/04/01' 
    assert l[4]=='2004/05/09'
    assert l[5]=='2005/06/15'
    assert l[6]=='2006/07/03'
    assert l[7]=='2007/08/18'
    assert l[8]=='2008/09/30'
    assert l[9]=='2009/10/31'
    assert l[10]=='2010/11/01'
    assert l[11]=='2011/07/05'


if __name__ == "__main__": 
    
    test_collect_d() # used to assert that find_dates workes
    html_str_Rowling= get_html("https://en.wikipedia.org/wiki/J._K._Rowling")
    html_str_fineman= get_html("https://en.wikipedia.org/wiki/Richard_Feynman")
    html_str_rosling = get_html("https://en.wikipedia.org/wiki/Hans_Rosling")
    find_dates(html_str_Rowling, "rowling_dates.txt")
    find_dates(html_str_fineman, "fineman_dates.txt")
    find_dates(html_str_rosling, "rosling_dates.txt")

