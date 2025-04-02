import os
import json
from scan_reseau import scan_reseau
from scan_vulnerabilites import scan_vulnerabilites
from generate_map import generer_carte_reseau

# Définition des chemins des fichiers de sortie
RESULTS_DIR = "data"
NETWORK_SCAN_FILE = os.path.join(RESULTS_DIR, "resultats_reseau.json")
VULN_SCAN_FILE = os.path.join(RESULTS_DIR, "resultats_vulnerabilites.json")

def sauvegarder_resultats(resultats, fichier):
    """Sauvegarde les résultats dans un fichier JSON."""
    with open(fichier, "w") as f:
        json.dump(resultats, f, indent=4)

def main():
    print("\n🚀 Démarrage du programme de cartographie réseau\n")

    # Étape 1 : Scanner le réseau
    ip_range = input("Entrez la plage d'adresses IP à scanner (ex: 192.168.1.0/24) : ")
    resultats_reseau = scan_reseau(ip_range)
    sauvegarder_resultats(resultats_reseau, NETWORK_SCAN_FILE)
    print(f"✅ Scan réseau terminé. Résultats sauvegardés dans {NETWORK_SCAN_FILE}")

    # Étape 2 : Scanner les vulnérabilités
    resultats_vulnerabilites = scan_vulnerabilites(ip_range)
    sauvegarder_resultats(resultats_vulnerabilites, VULN_SCAN_FILE)
    print(f"✅ Scan des vulnérabilités terminé. Résultats sauvegardés dans {VULN_SCAN_FILE}")

    # Étape 3 : Générer la carte du réseau
    print("\n📍 Génération de la carte du réseau...")
    generer_carte_reseau()
    print("✅ Carte du réseau générée.")

if __name__ == "__main__":
    main()