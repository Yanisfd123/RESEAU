import json
import networkx as nx
import matplotlib.pyplot as plt
import math

def charger_donnees(fichier):
    with open(fichier, "r") as f:
        return json.load(f)

def generer_carte_reseau():
    print("📍 Génération de la carte du réseau en forme de soleil...")

    appareils = charger_donnees("data/resultats_reseau.json")
    G = nx.Graph()
    
    # Ajout du noeud central représentant le réseau
    centre_reseau = "Mon Réseau"
    G.add_node(centre_reseau, color="gold", size=5000)
    
    pos = {centre_reseau: (0, 0)}  # Position centrale
    
    # Calcul des positions en cercle autour du centre
    nb_appareils = len(appareils)
    angle_step = 2 * math.pi / nb_appareils if nb_appareils > 0 else 0
    
    for i, appareil in enumerate(appareils):
        ip = appareil["ip"]
        G.add_node(ip, color="lightblue")
        
        # Position en cercle autour du centre
        angle = i * angle_step
        distance = 2  # Distance du centre
        pos[ip] = (distance * math.cos(angle), distance * math.sin(angle))
        
        # Connexion au centre
        G.add_edge(centre_reseau, ip)
        
        # Ajout des ports sous chaque IP (en descendant)
        nb_ports = len(appareil["ports_ouverts"])
        for j, port in enumerate(appareil["ports_ouverts"]):
            port_node = f"{ip}\nPort {port}"
            G.add_node(port_node, color="lightgreen", size=800)
            
            # Position sous l'IP avec un décalage
            port_distance = distance + 1 + j * 0.3
            pos[port_node] = (port_distance * math.cos(angle), 
                             port_distance * math.sin(angle) - j * 0.2)
            
            G.add_edge(ip, port_node)

    # Préparation des couleurs et tailles
    colors = [G.nodes[n].get('color', 'gray') for n in G.nodes]
    sizes = [G.nodes[n].get('size', 1000) for n in G.nodes]
    
    plt.figure(figsize=(12, 12))
    nx.draw_networkx(
        G, pos, 
        with_labels=True, 
        node_color=colors,
        node_size=sizes,
        font_size=7,
        edge_color="gray",
        alpha=0.8,
        linewidths=0.5
    )
    
    # Dessiner un cercle autour du noeud central pour l'effet "boule"
    centre_circle = plt.Circle(pos[centre_reseau], 0.3, color='gold', alpha=0.4)
    plt.gca().add_patch(centre_circle)
    
    plt.title("Carte du Réseau - Topologie en Soleil", pad=20)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generer_carte_reseau()