#Query PubMed for all articles having to do with "author's last name" and check first how many of such articles there are:

from Bio import Entrez

# Always tell NCBI who you are
Entrez.email = "sunheejung@gmail.com"
handle = Entrez.egquery(term="Goodlett")
record = Entrez.read(handle)
for row in record["eGQueryResult"]:
    if row["DbName"]=="pubmed":
        countpubmed = row["Count"]
        print row["Count"] + " records found"
        print "Please Wait..."

# use the Bio.Entrez.efetch function to download the PubMed IDs of these #(countpubmed) articles
handle = Entrez.esearch(db="pubmed", term="Goodlett", retmax=countpubmed)
record = Entrez.read(handle)
idlist = record["IdList"]
#print idlist

#download the Medline records in the Medline falt-file format, and use the Bio.Medline module to parse them
from Bio import Medline
handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
records = Medline.parse(handle)
records = list(records)

#for record in records:
#    print "title:", record["TI"]
#    print "authors:", record["AU"]
#    print "source:", record["SO"]

#search for a particular author, split data, and save them to a dictionary called "years"    
search_author = "Goodlett DR"
years = {}
for record in records:
    if not "AU" in record:
        continue
    if search_author in record["AU"]:
        date = record["DP"]
        year = date.split();
	#print year[0]
        if years.has_key(year[0]):
            years[year[0]] = years[year[0]] + 1
        else:
            years[year[0]] = 1
        #print "Author %s found: %s" % (search_author, record["SO"])

#make a bar graph for the number of articles per year for a particular author using Google chart
keys = years.keys()
keys.sort()
#print keysA
url = "https://chart.googleapis.com/chart?cht=bvs&chs=800x200&chtt=Publications|by|Year&chxt=x,y"
data = "&chd=t:"
text = "&chxl=0:"
while keys:
	current_year = keys.pop()
	text += "|" + str(current_year)
	data += str(years[current_year]) + ","
url = url + text + data
url = url[:-1]
print url
