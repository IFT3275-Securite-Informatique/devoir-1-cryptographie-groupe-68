import math
import random as rnd
import numpy as np
import requests
from collections import Counter



# Chargement du texte depuis les fichiers du Project Gutenberg
def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gérer les erreurs de connexion
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading the text: {e}")
        return None

# Diviser un texte en paires de caractères (bicaractères)
def cut_string_into_pairs(text):
    pairs = []
    for i in range(0, len(text) - 1, 2):
        pairs.append(text[i:i + 2])
    if len(text) % 2 != 0:
        pairs.append(text[-1] + '_')  # Ajouter un caractère de remplacement si impair
    return pairs

# Charger le texte depuis Project Gutenberg
url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
text = load_text_from_web(url)
url2 = "https://www.gutenberg.org/ebooks/4650.txt.utf-8"
text += load_text_from_web(url2)

# Extraire les caractères uniques
caracteres = list(set(list(text)))
nb_caracteres = len(caracteres)
nb_bicaracteres = 256 - nb_caracteres
bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(text)).most_common(nb_bicaracteres)]
symboles = caracteres + bicaracteres
nb_symboles = len(symboles)

# Générer la clé de substitution
def gen_key(symboles):
    l = len(symboles)
    if l > 256:
        return False

    rnd.seed(1337)
    int_keys = rnd.sample(list(range(l)), l)
    dictionary = {s: "{:08b}".format(k) for s, k in zip(symboles, int_keys)}
    return dictionary

# Générer la clé de chiffrement
K = gen_key(symboles)

# Fonction d'inversion de la clé pour le déchiffrement
def invert_key(key):
    return {v: k for k, v in key.items()}

# Fonction de déchiffrement
def symboles_vers_M(C, K_inv):
    decoded_text = []
    i = 0
    
    while i < len(C):
        # Vérifier les symboles de 8 bits (octets)
        octet = C[i:i+8]
        if octet in K_inv:
            decoded_text.append(K_inv[octet])
            i += 8  # Passer aux 8 bits suivants
        else:
            decoded_text.append('?')  # Placeholder pour caractères non déchiffrés
            i += 8
    return ''.join(decoded_text)

def decrypt(C, K):
    K_inv = invert_key(K)
    M = symboles_vers_M(C, K_inv)
    return M

"""""
# Exemple de message à chiffrer et déchiffrer
M = text[10000:10100]  # Choisir un extrait de texte
def chiffrer(M, K):
    l = [K.get(s, '?') for s in M]
    return ''.join(l)

C = chiffrer(M, K)  # Message chiffré
M_dechiffre = decrypt(C, K)  # Message déchiffré

print("Message original :", M)
print("Message chiffré :", C)
print("Message déchiffré :", M_dechiffre)
"""
