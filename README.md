# Maze-Path-Finding

Les différents algorithmes ont leurs propres dossiers, dans lesquels se trouvent les labyrinthes de test.

## AStart

Dans le dossier Astart se trouve un algorithme de type AStar que vous pouvez lancer avec la commande :  
*python Astart.py <nom_laby> <nom_pos>*  
*<nom_laby>* étant l'image du labyrinthe  
*<nom_pos>* étant un fichier xml spécifiant les position du point départ et de celui  d'arrivée (facultatif).

Exemple de fichier <nom_pos> :  
![alt text][posExample]

### Détection automatique des points d'arrivée/départ
Si vous ne spécifiez pas de fichier de position, le programme va tenter de les trouver tous seuls en cherchant des pixels d'une certaines couleurs (par défaut rouge pour le départ et vert pour l'arrivée).

### Configuration
Dans le dossier ce trouve un fichier de configuration *config.xml* qui par défaut contient les informations suivantes :  
![alt text][config]


[posExample]:
https://github.com/Smookii/Maze-Path-Finding/Documentation/Image/PosExample.PNG "Exemple de fichier de position"


[config]:
https://github.com/Smookii/Maze-Path-Finding/Documentation/Image/config.PNG "config.xml"
