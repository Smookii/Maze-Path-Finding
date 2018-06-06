Utilisation de la VM : 

user : deb  
pwd : debbie  
pwd-root : debbie  

Avant tout, 

```shell
source activate traitement
```

# Maze-Path-Finding

Les différents algorithmes ont leurs propres dossiers, dans lesquels se trouvent les labyrinthes de test.

## Simple Maze Solver
Dans le dossier SimpleMazeSolver se trouve un algorithme utilisant le connected component labeling pour résoudre un labyrinthe, il se lance avec la commande suivante :

*python mazeSolveSimple.py <nom_laby>*  
*<nom_laby>* étant l'image du labyrinthe.

L'idée de l'algorithme vient de [ce site](http://www.crisluengo.net/index.php/archives/277).

### Fonctionnement
Cet algorithme est capable de résoudre nimporte quel labyrinthe simple c'est à dire ne comportant que 2 parties interconnectées. Pour se faire l'algorithme utilise la fonction `connectedComponents(img)` d'openCV qui permet de marquer les différentes zone de l'image qui sont interconnectées donc dans notre cas nous auront deux zones marquées:
![alt text][connectedComponent]

On peut facilement remarquer que la solution du labyrinthe se trouve entre les deux zones colorées. Il suffit donc de dilater l'une des zone et de soustraire la zone a cette dilatation pour obtenir une solution. Il est important de noter que si le labyrinthe est plus complexe donc qu'il a plus de deux zones interconnectées cet algorithme ne marche plus. Le dossier SimpleMazeSolver contient deux images de labyrinthe avec lesquels cet algorithme marche.

## Skeletonize Maze Solve
Dans le dossier SkeletonizeSolver se trouve un algorithme utilisant la skeletonization pour résoudre un lanyrinthe, il se lance avec la commande suivante :

*python SkeletonizeMazeSolve.py <nom_laby>*  
*<nom_laby>* étant l'image du labyrinthe.

L'idée de l'algorithme vient de [ce site](http://www.crisluengo.net/index.php/archives/277).

### Fonctionnement
L'algorithme utilise une fonction de skeletonization afin de définir tous les chemin possible du labyrinthe:
![alt text][Skelet]

Ensuite l'idée est de repérer les deadEnd de ce labyrinthe c'est à dire les pixel qui correspondent à des culs de sac et de supprimer itérativement les chemin menant a ces culs de sac. Pour se faire on parcour les pixel depuis les deadEnd et on supprime chaque pixel qui n'est connecté qu'à un pixel et de cette manière on supprime les chemins ne menant à rien. Il faut noter que le départ et la fin du labyrinthe doivent être enlevé de la liste des deadEnd pour ne pas supprimer des chemin valides. Pour se faire on donne leur position dans le fichier param.xml.

Après cette première étape il ne reste plus que des chemins valides et il suffirait d'utiliser un algorithme du genre d'Astar pour définir le chemin le plus cour et ne garder que celui-ci. Mais malheureusement l'étape de suppression des deadEnd ne marche pas assez bien dans notre implémentation pour qui ne reste plus que des chemins valides. Cela vient surement du fait que le squelette obtenu par la fonction `morphology.skeletonize()` de skimage ne donne pas un squelette d'aussi bonne qualité que dans ce [exemple](http://www.crisluengo.net/index.php/archives/277) (fonction bskeleton de MATLAB). Nous avons quand même mis à disposition le script avec un exemple d'image même s'il n'est pas totalement fonctionnel afin de donner une idée du fonctionnement.

## AStar

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

**SUAREFIND**   
Détermine comment l'algorithme va rechercher le chemin vers la sortie à True le chemin sera recherché sur tous les pixels adjaçant diagonales inclusent :   

|      |          |        |          |       |
| :-----------: | :-------------: | :------------: | :-------------: | :------------: |
| 3 | 3 | 3 | 3 | 3 |
| 3 | 2 | 2 | 2 | 3 |
| 3 | 2 | 1 | 2 | 3 |
| 3 | 2 | 2 | 2 | 3 |
| 3 | 3 | 3 | 3 | 3 |

Si on le laisse vide les diagonales ne seront pas inclusent :

|      |          |        |          |       |
| :-----------: | :-------------: | :------------: | :-------------: | :------------: |
| 5 | 4 | 3 | 4 | 5 |
| 4 | 3 | 2 | 3 | 4 |
| 3 | 2 | 1 | 2 | 3 |
| 4 | 3 | 2 | 3 | 4 |
| 5 | 4 | 3 | 4 | 5 |

**COLORTEINT**   
A True les pixels que l'algoritme à traverser auront une teinte dégradé ce qui peux simplifier l'observation du labyrinthe. Laisser vide les pixels auront une couleur unie.



**ANIMATION.first**   
A "1" l'attribut permet d'afficher tous le déroulement de la partie de recherche, à "0" l'algorithme ne s'affichera qu'une fois déroulé.

**ANIMATION.second**   
A "1" l'attribut permet d'afficher tous le déroulement de la partie de retour, à "0" l'algorithme ne s'affichera qu'une fois déroulé.

**ANIMATIONDELAY**   
Permet de gérer la fréquence d'affichage du déroulement de l'algorithme, la valeurs du champs déterminera le nombre de d'itération de l'algorithme avant le raffrachissement.

**DISTANCEMAX**   
Ce paramètre détermine le nombre d'itérations maximum que l'algorithme va faire avant de s'arrêter. Ce qui déclenche l'erreur :   
*La distance max à été atteinte, réessayé en augmentant le DISTANCEMAX dans config.xml*

**BORDERSIZE**     
Ce paramètre permet de spécifié la taille minimum des murs du labyrinthe utilisé, ce qui permet à l'algorithme de faire de plus grands pas à chaque itérations.

**COLORDEP**   
Permet de définir les conditions de la couleur du pixel de départ, pour la recherche de position automatique.
Le paramètre *ref* permet déterminer qu'elle valeurs de couleur sera principale.   
Dans l'exemple de config, un pixel sera considéré comme point de départ si  :

pixel.bleu < 100   
pixel.green < 100   
pixel.red > 250   

**COLOREND**   
Permet de définir les conditions de la couleur du pixel de d'arrivée, pour la recherche de position automatique.  



[posExample]:
https://github.com/Smookii/Maze-Path-Finding/blob/master/Documentation/Image/PosExample.PNG "Exemple de fichier de position"


[config]:
https://github.com/Smookii/Maze-Path-Finding/blob/master/Documentation/Image/config.PNG "config.xml"

[Skelet]:
https://github.com/Smookii/Maze-Path-Finding/blob/master/Documentation/Image/skel.png "squelette d'un labyrinthe"

[connectedComponent]:
https://github.com/Smookii/Maze-Path-Finding/blob/master/Documentation/Image/connectedComponent.PNG "Exemple d'étiquetage d'un labyrinthe"

## Naive Wall Follower

A l'instar du simple maze solver, ce programme résouds les labyrinthes simples composées de 2 parties interconnectées. L'algorithme est simple et se contente de suivre continuellement le mur de droite (Solution naïve qui marche néanmoins dans un cas réel. 

### Fonctionnement 

L'algorithme commence par parcourir les bords du labyrinthe afin de trouver une entrée : il détermine en suite la direction de base à parcourir. A chaque itération, l'état de la case à droite et de devant (relativement à sa direction) est examinée. 

```python
...
RELATIVERIGHT = {
	'right' : (1, 1)
	'left' : (-1, -1)
	'up' : (1, -1)
	'down' : (-1, 1)
}

index_r = RELATIVERIGHT[direction]
index = DIRECTION[direction]

...
```
La direction a adopter ensuite est determinée en conséquence.

Les points par lequels l'algo passe sont stockés pour le playback.

### Utilisation

python wall_follower.py <filename> <speed>


- un premier enter montre l'image traitée (seuillage, élimination du bruit)
- un deuxième enter montre la solution trouvée.

### Condition du labyrinthe

Le chemin doit être de couleur claire, et les murs d'une couleur fonçée. Les entrées doivent être directement présentes dans les bords de l'image (pas d'espace entre le cadre de l'image et le cadre du labyrinthe)

### Exemple

ex : python wall_follower.py maze_solution_03.png 10
