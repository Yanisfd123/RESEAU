import nmap
import json
import os

VULN_DB_FILE = "vulnerabilities_db.json"

def charger_base_vulnerabilites():
    if not os.path.exists(VULN_DB_FILE):
        raise FileNotFoundError(f"Le fichier {VULN_DB_FILE} est introuvable")
    
    with open(VULN_DB_FILE, "r") as f:
        return json.load(f)

def scan_vulnerabilites(ip_range):
    nm = nmap.PortScanner()
    print(f"🔍 Scan des vulnérabilités sur {ip_range}...")

    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)

    vuln_db = charger_base_vulnerabilites()
    nm.scan(hosts=ip_range, arguments="-p " + ",".join(vuln_db.keys()) + " --open")

    resultats = []
    for host in nm.all_hosts():
        ports_ouverts = []
        
        for port in nm[host].all_tcp():
            if nm[host]['tcp'][port]['state'] == 'open':
                desc = vuln_db.get(str(port), "Inconnu")
                ports_ouverts.append({
                    "port": port,
                    "description": desc
                })

        if ports_ouverts:
            resultats.append({
                "ip": host,
                "vulnerabilites": ports_ouverts
            })

    # Sauvegarder dans le fichier spécifique
    with open("data/resultats_vulnerabilites.json", "w") as f:
        json.dump(resultats, f, indent=4)

    return resultats

ip_range = input("Entrez l'adresse IP ou la plage d'adresses IP à scanner : ")
resultats = scan_vulnerabilites(ip_range)