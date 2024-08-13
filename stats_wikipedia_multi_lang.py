# -*- coding: utf-8 -*-
# input: txt file with two columns: qcode;name
# Q34253;Linus Torvalds
# Q1362152;Michael Widenius
# Q6348774;Kaj Arnö
# Q330874;Mårten Mickos

# possible improvement would be to use the wikidata API to get the titles in all languages

from mwviews.api import PageviewsClient
from datetime import datetime
import datetime as dt
import urllib.request
import re
import pandas as pd

#langs = ["af", "an", "ang", "ar", "ast", "az", "bar", "be-tarask", "be", "bg", "bn", "br", "bs", "ca", "ckb", "cs", "da", "de", "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fr", "fur", "fy", "ga", "gd", "gl", "gu", "he", "hi", "hr", "ht", "hu", "hy", "ia", "id", "io", "is", "it", "ja", "jbo", "jv", "ka", "ki", "kk", "km", "kn", "ko", "ku", "ky", "la", "lad", "lb", "li", "lmo", "ln", "lt", "lv", "mai", "mg", "mk", "mn", "mr", "ms", "myv", "nds", "new", "nl", "nn", "no", "oc", "or", "pa", "pl", "pt", "ru", "sv", "tr", "zh", "ro", "sa", "sah", "sc", "scn", "sd", "sh", "si", "simple", "sk", "sl", "so", "sq", "sr", "szl", "ta", "te", "tet", "tg", "th", "tl", "uk", "ur", "vi", "war", "wuu", "yi", "zh-min-nan", "zh-yue", "arz", "ml"]
#langs = ["sv", "fi", "en", "de", "fr", "es", "it", "nn", "no", "nl", "cs", "eo", "pl", "hr", "hy", "sh", "tr", "uk", "ru", "ar", "arz", "ta","mg","ko"]
#langs = ["ru"]
#langs = ["sv","fi","en","de","fr","no","da","uk","ru"]
#langs = ["sv","fi","en","de","fr","no","da","uk","ru"]
langs = ["sv","fi","en","de","fr","uk","ru","pl","et"]
platform = "wikipedia"

path = "/Users/robertsilen/Python/Roberts-Wikiverktyg/forum/"
input = "forum_ort.txt"
output = "forum_tema_output.xlsx"
#input = "ukraina.txt"
#output = "ukraina-output.xlsx"
#input = "input-finsvetekn.csv"
#input = "input-konecranes.txt"
#input = "input-finlandkrig.csv"
#input = "input-test2.txt"
#input = "input-test3.txt"
#input "input-ukraina.txt"
#input = "voronoi backlist - wd.txt"


now1 = datetime.now()
current_time1 = now1.strftime("%H:%M:%S")
print(f"\nStarting at {current_time1}")

def readfile(path, filename):
    fullpath = path + filename
    print(f"Reading: {fullpath}")
    file = open(fullpath, "r")
    data = file.read()
    rows = data.split("\n")
    datalist = []
    for i, row in enumerate(rows):
        #print(len(row.split(";")))
        print(i)
        if(len(row.split(";"))>=1):
            datalist.append(row.split(";"))
        else:
            print("Error in input file: correct format for each row is qcode;name. Remember to remove empty rows.")
            exit()
    file.close()
    return datalist

def writefile(s, path, filename):
    fullpath = path + filename
    print(f"Writing: {fullpath}")
    text_file = open(fullpath, "w")
    text_file.write(s)
    text_file.close()

def writeexcel(dfs, path, filename):
    fullpath = path + filename
    print(f"Writing: {fullpath}")
    i=1
    with pd.ExcelWriter(fullpath) as writer:
        for df in dfs:
            df.to_excel(writer, sheet_name=f'Sheet{i}')

def views_by_article(lang, platform, article):
    p = PageviewsClient(user_agent="<kaj@projektfredrika.fi>")
    wikipedia = f'{lang}.{platform}'
    try:
        fresh = p.article_views(wikipedia, article, start='20220101', end='20221231')
        c_fresh = 0
        for row in fresh:
            if fresh[row][article] != None:
                c_fresh += fresh[row][article]
        return c_fresh 
    except Exception as e:
        print(f"Error getting views: {lang} {article} {e}")
        return "error"

def length_by_article(lang, platform, article):
    article = urllib.parse.quote(article)
    url = f"https://{lang}.{platform}.org/w/api.php?action=query&format=json&titles={article}&prop=revisions&rvprop=size"
    mystr = ""
    try:
        length = 0
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close
        length = re.findall("\"size\":[0-9]*",mystr)
        length = re.findall("[0-9]+",length[0])[0]
        return length
    except Exception as e:
        print(f"Error getting length: {lang} {article}")
        return "error"

def title_by_lang(q_code):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&format=xml&props=sitelinks&ids={q_code}&sitefilter=xxwiki"
    mystr = ""
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
    except Exception as e:
        print(e)
    languages = []
    for i, row in enumerate(mystr.split('<sitelink site="')):
        if i == 0:
            continue
        wiki, skip1, title, skip2 = row.split('"')
        language = re.fullmatch("[a-z][a-z][a-z]?wiki",wiki)
        if not language:
            continue
        title = title.replace("&#039;", "'") 
        title = title.replace("&quot;", '"')
        title = title.replace(" ", "_")
        language = language.group(0).replace("wiki","")
        languages.append([language, title])
    return languages

inputrows = readfile(path, input)
print(inputrows)

# skapar data för voronoi
v = f"wikidata-code\tlabel\tlang\tlang-i\twikipedia-article\tviews\tlength\n"
p = []

# skapar data med sammandrag
s = f"wd-q-code;label-uk;label-en"
a = []
b = ["wd-q-code","label-uk","label-en"]

for i, lang in enumerate(langs): 
    s += f";{lang}-views;{lang}-length"
    b.append(f"{lang}-views")
    b.append(f"{lang}-length")
s += "\n"
a.append(b)

# skapar excel fil med sammandrag
print(f"Rows in input: {len(inputrows)}")
i=0
for qcode, label_uk, label_en in inputrows: 
    i = i+1
    s += f"{qcode}; {label_uk}; {label_en}" 
    b = [qcode,label_uk,label_en]

    articles = title_by_lang(qcode)
    now2 = datetime.now()
    current_time2 = now2.strftime("%H:%M:%S")
    print(f"\n{current_time2}: Fetching {i}/{len(inputrows)}: {qcode} {label_uk}, {label_en}")

    for langi, lang in enumerate(langs): 
        articlename = ""
        views = ""
        length = ""
        for article in articles:
            if article[0]==lang:
                articlename = article[1]
                views = views_by_article(lang, platform, articlename)
                length = length_by_article(lang, platform, articlename)
        s += f"; {views}; {length}"
        b.append(views)
        b.append(length)
        v += f"{qcode}\t{label_uk}\t{label_en}\t{lang}\t{langi+1}\t{articlename}\t{views}\t{length}\n"
        p.append([qcode,label_uk,label_en,lang,articlename,views,length])
        print(f"{qcode};{label_uk};{label_en};{lang};{articlename};{views};{length}")
    s += "\n"
    a.append(b)
    writefile(s, path, "output-summary.csv")
    writefile(v, path, "output-data.tsv")
    df1 = pd.DataFrame(p, columns = ["wikidata-code","label-uk","label-en","lang","wikipedia-article","views","length"])
    df2 = pd.DataFrame(a)
    df2.rename(columns=df2.iloc[0, :], inplace=True) 
    df2.drop(df2.index[0], inplace=True)
    print(f"Writing: {path+output}")
    with pd.ExcelWriter(path+output) as writer:
        df1.to_excel(writer, sheet_name='VoronoiData')
        df2.to_excel(writer, sheet_name='Summary')

#print(s)
#print(v)
#writefile(s, path, "output-summary.csv")
#writefile(v, path, "output-data.tsv")

#df1 = pd.DataFrame(p, columns = ["wd-kod","wd-etikett","lang","wp-artikel","visningar","längd"])
#df2 = pd.DataFrame(a)
#df2.rename(columns=df2.iloc[0, :], inplace=True) 
#df2.drop(df2.index[0], inplace=True)

now2 = datetime.now()
current_time2 = now2.strftime("%H:%M:%S")
diff = now2 - now1 

#print(f"\nWriting {path+output}")
#with pd.ExcelWriter(path+output) as writer:
    #df1.to_excel(writer, sheet_name='Summary')
    #df2.to_excel(writer, sheet_name='Data')
print(f"{len(inputrows)} objects processed from {current_time1} to {current_time2} in {diff}.")
