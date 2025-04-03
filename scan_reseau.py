import nmap
import json
import os

def scan_reseau(ip_range):
    nm = nmap.PortScanner()
    print(f"🔍 Scan en cours sur {ip_range}...")

    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)

    nm.scan(hosts=ip_range, arguments="-p- --open")

    resultats = []
    for host in nm.all_hosts():
        etat = nm[host].state()
        ports_ouverts = []
        
        for port in nm[host].all_tcp():
            if nm[host]['tcp'][port]['state'] == 'open':
                ports_ouverts.append(port)
        
        resultats.append({
            "ip": host,
            "etat": etat,
            "ports_ouverts": ports_ouverts
        })

    # Sauvegarder dans le fichier spécifique
    with open("data/resultats_reseau.json", "w") as f:
        json.dump(resultats, f, indent=4)

    return resultats

