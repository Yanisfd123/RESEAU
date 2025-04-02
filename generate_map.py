import json
import networkx as nx
import matplotlib.pyplot as plt

def charger_donnees(fichier):
    with open(fichier, "r") as f:
        return json.load(f)

def generer_carte_reseau():
    print("📍 Génération de la carte du réseau...")
    
    appareils = charger_donnees("data/resultats_reseau.json")
    vulnerabilites = charger_donnees("data/resultats_vulnerabilites.json")
    G = nx.Graph()
    
    vuln_dict = {(v["ip"], item["port"]): item["description"] 
                 for v in vulnerabilites for item in v["vulnerabilites"]}
    
    for appareil in appareils:
        ip = appareil["ip"]
        G.add_node(ip, color='green')
        for port in appareil["ports_ouverts"]:
            port_node = f"Port {port}"
            G.add_node(port_node, color='blue')
            G.add_edge(ip, port_node, desc=vuln_dict.get((ip, port), ""))
    
    pos = nx.spring_layout(G, seed=42)
    colors = [G.nodes[n].get('color', 'gray') for n in G.nodes]
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=3000, edge_color="black", font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "desc"), font_size=8)
    
    plt.title("Carte du Réseau avec Vulnérabilités")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    generer_carte_reseau()
