
file = open('projet.txt', 'r')
Lines = file.readlines()

import csv
from mdtable import MDTable
import os

def getAfter(text, word):    #fonction qui permet de capturer le mots apres d'un caractere donnee 
	splited = text.split(word,1)
	if len(splited) > 0:
		return text.split(word,1)[1].strip().split(' ')[0].strip()
	else:
		return ''

def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

class request:
	def __init__(self, hour, source, dest, flag, length, protocol):
		self.hour = hour
		self.source = source
		self.dest = dest
		self.flag = flag
		self.length = length
		self.protocol = protocol
 
requests = []
lines = []
for line in Lines:
	if not line.startswith((' ', '\t')) and "Flags" in line: #si la ligne ya pas un tab et de flag elle n'est pas compté 
		requests.append(request(line.strip().split(' ')[0],
			getAfter(line, line.strip().split(' ')[1]),
			getAfter(line, ">").replace(':', ''), #adresse destination 
			getAfter(line, "Flags").replace('[', '').replace('],', ''), # Flags [P.], supprime la virgule apres le mots 
			getAfter(line, "length").replace(':', ''),
			line.strip().split(' ')[1]))

with open('result.csv', 'w', encoding='UTF8') as f: # cree le fichier resultat en .csv
	writer = csv.writer(f)
	writer.writerow(['Hour', 'Source', 'Destination', 'Flag', 'Length', 'Protocol'])
	for req in requests:
		writer.writerow([req.hour, req.source, req.dest, req.flag, req.length, req.protocol])

remove_empty_lines("result.csv") # enleve les lignes vides sur le fichier csv

markdown_string_table = MDTable('result.csv').get_table()
f = open("result.md", "w")
f.write(markdown_string_table)
f.close()


