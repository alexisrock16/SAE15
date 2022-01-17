
file = open('projet.txt', 'r')	#ouvre le fichier log projet
Lines = file.readlines()



import csv
import markdown
from mdtable import MDTable
import os

def getAfter(text, word):    #fonction qui permet de capturer le mots apres d'un caractere donnee 
	splited = text.split(word,1)
	if len(splited) > 0:
		return text.split(word,1)[1].strip().split(' ')[0].strip()
	else:
		return ''

def remove_empty_lines(filename): 		 # enleve les lignes vides sur le fichier csv  resultat de la fonction 
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

class request:				# utiliser les classes sont un moyen de reunir des données
	def __init__(self, heure, source, dest, flag, length, protocol): #initialise les variables
		self.heure = heure 
		self.source = source
		self.dest = dest
		self.flag = flag
		self.length = length
		self.protocol = protocol

requests = []
lines = []
for line in Lines:
	if not line.startswith((' ', '\t')) and "Flags" in line: #si la ligne ya pas un tab et de flag elle n'est pas compté 
		requests.append(request(line.strip().split(' ')[0], #heure
			getAfter(line, line.strip().split(' ')[1]), #source
			getAfter(line, ">").replace(':', ''), #adresse destination 
			getAfter(line, "Flags").replace('[', '').replace('],', ''), # Flags [P.], supprime la virgule apres le mots 
			getAfter(line, "length").replace(':', ''),	#capture la taille si elle y es et surprime les ":" par rien
			line.strip().split(' ')[1]))

with open('result.csv', 'w', encoding='UTF8') as f: # cree le fichier resultat en .csv
	writer = csv.writer(f)
	writer.writerow(['heure', 'Source', 'Destination', 'Flag', 'Length', 'Protocole'])
	for req in requests:
		writer.writerow([req.heure, req.source, req.dest, req.flag, req.length, req.protocol])

remove_empty_lines("result.csv") # enleve les lignes vides sur le fichier csv resultat de la fonction 




markdown_string_table = MDTable('result.csv').get_table() # cree un tableau markdown a pârtir du fichier
f = open("result.md", "w")
f.write(markdown_string_table)
f.close()

with open("result.md",'r') as f:
    text=f.read()
    html=markdown.markdown(text,extensions=['tables']).replace("<table>", '<table class="table table-striped">') #permet de replacer la variable qui contient table dans 'table table-striped' ce qui nous permet davoir de mettre en css sans toucher le variable deja presente dans le css bootstrap
    with open('index.html','w') as f: #cree et ecrit le fichier index.html qui permet davoir une page web contenant toute les donnes du fichier md deja cree
        f.write("""<!DOCTYPE html>			
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pecheric site sae15</title>
		

            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" >
        </head>
		<header> <h1> Voici les donnees triees du fichier de log </h1>  </header>
		<style> h1 {
			text-align:center;
		}</style>
        <body>"""+html+"""<div style="width: 100%; display: flex; justify-content:center;align-items:center"><img onclick="window.scrollTo(0,0)" class="bonjour" src=""/></div></body>
        
		</html>""")