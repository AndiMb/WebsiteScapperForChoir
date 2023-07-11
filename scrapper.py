import csv
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import configparser

# Read Config File
config = configparser.ConfigParser()
config.read('config.ini')

numThreads = int(config['General']['numThreads'])
bundesland = config['General']['Bundesland']

schoolsFile = config[bundesland]['schoolsFile']
schulnamecolumn = int(config[bundesland]['schulnamecolumn'])
ulrcolumn = int(config[bundesland]['ulrcolumn'])
delimiterChar = config[bundesland]['delimiterChar']
quotecharChar = config[bundesland]['quotecharChar']
datadir = config[bundesland]['datadir']
LinkExtDenyRegex = config[bundesland]['LinkExtDenyRegex']

numberColumnsOrig = 0

# Clean the URL, e.g. from Whitespaces
def cleanURL(url):
    cleanurl = str(url).strip()
    if not re.match('(?:http|ftp|https)://', cleanurl):
        cleanurl = 'http://{}'.format(cleanurl)
    return cleanurl

def getDomainFromURL(url):
    return url.replace("https://","").replace("http://","").split("/",1)[0]

def getFilenameFromURL(url):
    return url.replace("https://","").replace("http://","").strip("/").replace("/","_")

# method to be called for each school / CSV row from file in parallel
def handleSchool(row):
    # if School has URL/Website
    if row[ulrcolumn] and not "(" in row[ulrcolumn] and not " " in row[ulrcolumn].strip():

        # cleanup URL
        url = cleanURL(row[ulrcolumn])

        # get Domain from URL
        domain = getDomainFromURL(url)
        
        # get Filename from URL
        filename = getFilenameFromURL(url)

        # run Scapy for URL
        os.system("cd wordlist_scrapper; scrapy crawl webcrawler" + 
                  " -a adomain=" + domain + 
                  " -a surls="+ url + 
                  " -a adeny=\""+ LinkExtDenyRegex + "\"" +
                  " -s CLOSESPIDER_TIMEOUT=120" + 
                  " > ../" + datadir + "/" + filename + ".link" + 
                  " 2> ../" + datadir + "/" + filename + ".log")
        
        # Count Links in resulting link file
        count = 0
        with open(datadir+"/" + filename + ".link", 'r') as fp:
            for count, line in enumerate(fp):
                pass
            if os.path.getsize(datadir + "/" + filename + ".link") > 0:
                count = count + 1
            else:
                count = 0
        
        # append number of found link to a extended CSV row
        row.append(count)
    else:
        # if no URL is available append 0 links to a extended CSV row
        row.append(0)
    return row

# Schools list
schools = []

# create result directory if not exists
if not os.path.exists(datadir):
    os.makedirs(datadir)

# open result files
with open(datadir + '/schools.csv', 'w') as outcsvfile, open(datadir + '/00_all.dat', 'w') as outdatfile:
    
    # create writer for extended CSV file
    writer = csv.writer(outcsvfile, delimiter=',', quotechar='"')

    # open schools file
    with open(schoolsFile, newline='') as csvfile:
        if len(quotecharChar) > 0:
            schoolreader = csv.reader(csvfile, delimiter=delimiterChar, quotechar=quotecharChar)
        else:
            schoolreader = csv.reader(csvfile, delimiter=delimiterChar)
        
        # handle headers
        header = next(schoolreader, None)

        # append last column
        header.append("choir")

        # write header to result file
        writer.writerow(header)

        numberColumnsOrig = len(header)-1

        for row in schoolreader:
            schools.append(row)

    # Start threadpool with number of threads
    with ThreadPoolExecutor(numThreads) as executor:

        # results list
        futures = []

        # put thread for school handling in pool
        for school in schools:
            futures.append(executor.submit(handleSchool, school))

        # handle finished results
        for res in as_completed(futures):

            # Output schoolname and number of found links
            print(res.result()[schulnamecolumn], res.result()[numberColumnsOrig])

            # write row to result CSV
            writer.writerow(res.result())
            outcsvfile.flush()

            # if links available copy them in one file
            if int(res.result()[numberColumnsOrig]) > 0:
                outdatfile.write(res.result()[schulnamecolumn] + "\n")
                if res.result()[ulrcolumn]:
                    url = cleanURL(res.result()[ulrcolumn])
                    domain = getDomainFromURL(url)
                    filename = getFilenameFromURL(url)
                    with open(datadir + "/" + filename + '.link','r') as csvfile:
                        for line in csvfile:
                            outdatfile.write('    ' + line)
                    outdatfile.flush()
