import requests

url = "https://trouve-mot.fr/api/random"
response = requests.get(url).json()

mot = response[0]["name"]
mot_len = len(mot)
i = 0
liste_de_lettres_cacher = ['*'] * mot_len  # Créez une liste de '*' de la même longueur que le mot

while i < mot_len:
    lettre_donnee = input("Entrez une lettre du mot à deviner (indice " + response[0]["categorie"] + "): ")
    if len(lettre_donnee) != 1 or not lettre_donnee.isalpha():
        print("Veuillez entrer une seule lettre valide.")
        continue

    if lettre_donnee in mot:
        print("Tu as trouvé la lettre " + lettre_donnee)
        for j in range(len(mot)):
            if mot[j] == lettre_donnee:
                liste_de_lettres_cacher[j] = lettre_donnee
    else:
        print("Raté")

    print("Mot caché : " + ''.join(liste_de_lettres_cacher))

    if '*' not in liste_de_lettres_cacher:
        i=mot_len


def win():
    print("Tu as gagné ! Tu as trouvé le mot : " + mot)

if i >= mot_len:
    win()
else:
    print("Désolé, tu as perdu.")

