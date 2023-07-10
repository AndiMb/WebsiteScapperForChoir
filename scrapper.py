import csv
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Sachsen
#schulnamecolumn = 1
#ulrcolumn = 48
#datadir = 'dataset20230709_3'
#delimiterChar = ','
#quotecharChar = '"'

# Thüringen
schulnamecolumn = 0
ulrcolumn = 11
datadir = 'thueringen_20230710'
delimiterChar = ';'
quotecharChar = ''


numThreads = 100
clearHTMLPages = ["/start.html", 
                  "/home.html", 
                  "/schule.html", 
                  "/aktuelles.html", 
                  "/unsere-schule.html", 
                  "/startseite.html", 
                  "/grundschule-stenn.html", 
                  "/grundschule-weischlitz.html",
                  "/willkommen.html",
                  "/rundgang.html"]

def hyphen_split(a):
    if a.count("/") < 4:
        return a
    return "/".join(a.split("/", 4)[:4])

def cleanURL(url):
    cleanurl = str(url).strip()
    for clearpage in clearHTMLPages:
        cleanurl = cleanurl.replace(clearpage,"")
    if "cms.sachsen.schule" in cleanurl:
        cleanurl = hyphen_split(cleanurl)
    return cleanurl

def getDomainFromURL(url):
    return url.replace("https://","").replace("http://","").strip("/")

def getFilenameFromDomain(domain):
    return domain.replace("/","_")

def handleSchool(row):
    if row[ulrcolumn]:
        url = cleanURL(row[ulrcolumn])
        domain = getDomainFromURL(url)
        filename = getFilenameFromDomain(domain)

        os.system("cd wordlist_scrapper; scrapy crawl webcrawler -a adomain=" + domain.split("/",1)[0] + " -a surls="+ url + " -s CLOSESPIDER_TIMEOUT=120 > ../" + 
                datadir + "/" + filename + ".csv 2> ../" + datadir + "/" + filename + ".log")
        count = 0
        with open(datadir+"/" + filename + ".csv", 'r') as fp:
            for count, line in enumerate(fp):
                pass
            if os.path.getsize(datadir + "/" + filename + ".csv") > 0:
                count = count + 1
            else:
                count = 0
        row.append(count)
    else:
        row.append(0)
    return row

schools = []

with open(datadir + '/schulen_new.csv', 'w') as outcsvfile, open(datadir + '/00_all.dat', 'w') as outdatfile:
    writer = csv.writer(outcsvfile, delimiter=',', quotechar='"')

    with open(datadir + '/schulen.csv', newline='') as csvfile:
        #schoolreader = csv.reader(csvfile, delimiter=delimiterChar, quotechar=quotecharChar)
        schoolreader = csv.reader(csvfile, delimiter=delimiterChar)
        header = next(schoolreader, None)  # handle headers
        header.append("choir")
        writer.writerow(header)

        for row in schoolreader:
            schools.append(row)

    with ThreadPoolExecutor(numThreads) as executor:

        futures = []

        for school in schools:
            futures.append(executor.submit(handleSchool, school))

        for res in as_completed(futures):
            print(res.result()[schulnamecolumn], res.result()[ulrcolumn+1])
            writer.writerow(res.result())
            outcsvfile.flush()
            if int(res.result()[ulrcolumn+1]) > 0:
                outdatfile.write(res.result()[schulnamecolumn] + "\n")
                if res.result()[ulrcolumn]:
                    url = cleanURL(res.result()[ulrcolumn])
                    domain = getDomainFromURL(url)
                    filename = getFilenameFromDomain(domain)
                    with open(datadir + "/" + filename + '.csv','r') as csvfile:
                        for line in csvfile:
                            outdatfile.write('    ' + line)
                    outdatfile.flush()
