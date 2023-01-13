import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
import math
#region Initialisation

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Score
Score = 0

# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

# Création de l'environnement de jeu
TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);
# attention, on utilise TBL[x][y] 
        
LARGEUR = TBL.shape [0]
HAUTEUR = TBL.shape [1]

#region generateMaps

# placements des pacgums et des fantomes
# La fonction 'PlacementsGUM' parcourt la carte TBL et qui crée une nouvelle matrice GUM
# qui contient un 1 à chaque case où il y a un pac-gum sur la carte TBL.
# La matrice GUM est utilisée pour savoir où se trouvent les pac-gums sur la carte.

def generateGumMap():
    GUM = np.zeros(TBL.shape, dtype=np.int32)
    # GUM[4][3] = 1
    # GUM[1][1] = 1
    # Met un 1 quand il y a un bonbon
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if ( TBL[x][y] == 0):
                GUM[x][y] = 1
    return GUM

GUM = generateGumMap()   

def generateWeightMap():
    map = []
    for y in range(HAUTEUR):
        map.append([])
        for x in range(LARGEUR):
            map[y].append(1 if TBL[x][y] == 0 else math.inf)
    return map

def generateVisitedMap():
    map = []
    for y in range(HAUTEUR):
        map.append([])
        for x in range(LARGEUR):
            map[y].append(False)
    return map

def generateDistMap():
    map = []
    for y in range(HAUTEUR):
        map.append([])
        for x in range(LARGEUR):
            map[y].append(math.inf)
    return map

#endregion

# Initialisation de la position de départ de Pac-Man
PacManPos = [5,5]
PacManState = "GUM"

Ghosts  = []
Ghosts.append( [LARGEUR//2, HAUTEUR // 2 ,  "pink"  , "UP"] )
Ghosts.append( [LARGEUR//2, HAUTEUR // 2 ,  "orange", "UP"] )
Ghosts.append( [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  , "UP"] )
Ghosts.append( [LARGEUR//2, HAUTEUR // 2 ,  "red"   , "UP"] )         

#########################################################################
# Debug : ne pas toucher (affichage des valeurs autours dans les cases) #
#########################################################################

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info

#endregion

#region Affichage

###########################################################################
#                                                                         #
# Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section #
#                                                                         #
###########################################################################



ZOOM = 40 # taille d'une case en pixels
EPAISS = 12 # epaisseur des murs bleus en pixels
FRAMETIME = 50

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight)) # taille de la fenetre
Window.title("SMARTMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
   
def WindowAnim():
    PlayOneTurn()
    Window.after(FRAMETIME,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
    return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
    global anim_bouche
    
    def CreateCircle(x,y,r,coul):
        canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
    canvas.delete("all")
      
      
    # murs
    
    for x in range(LARGEUR-1):
        for y in range(HAUTEUR):
            if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
                xx = To(x)
                xxx = To(x+1)
                yy = To(y)
                canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR-1):
            if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
                xx = To(x) 
                yy = To(y)
                yyy = To(y+1)
                canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
                
    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if ( GUM[x][y] == 1):
                xx = To(x) 
                yy = To(y)
                e = 5
                canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
                
    #extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) 
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
            
    #extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y) 
            txt = TBL2[x][y]
            canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
    # dessine pacman
    xx = To(PacManPos[0]) 
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche+1)%len(animPacman)
    ouv_bouche = animPacman[anim_bouche] 
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
    canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
    
    #dessine les fantomes
    dec = -3
    for P in Ghosts:
        xx = To(P[0]) 
        yy = To(P[1])
        e = 16
        
        coul = P[2]
        # corps du fantome
        CreateCircle(dec+xx,dec+yy-e+6,e,coul)
        canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
        
        # oeil gauche
        CreateCircle(dec+xx-7,dec+yy-8,5,"white")
        CreateCircle(dec+xx-7,dec+yy-8,3,"black")
        
        # oeil droit
        CreateCircle(dec+xx+7,dec+yy-8,5,"white")
        CreateCircle(dec+xx+7,dec+yy-8,3,"black")
        
        dec += 3
      
    # texte  
    canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
    canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
    canvas.create_text(screeenWidth - 50, screenHeight- 20 , text = Score, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)

#endregion

#region Gestion de partie

###############################################################################
#                                                                             #
# Partie III :   Gestion de partie   -   placez votre code dans cette section #
#                                                                             #
###############################################################################

# Renvoie la liste des mouvements possibles de Pac Man
def PacManPossibleMoves():
    L = []
    x,y = PacManPos
    if ( TBL[ x ][y-1] == 0 ): L.append((0,-1))
    if ( TBL[ x ][y+1] == 0 ): L.append((0, 1))
    if ( TBL[x+1][ y ] == 0 ): L.append(( 1,0))
    if ( TBL[x-1][ y ] == 0 ): L.append((-1,0))  
    return L

def isInCorridor(x, y):
    # Regarder N cases plus loin plûtot que 1

    # couloir horizontal
    if TBL[x][y+1] != 0 and TBL[x][y-1] != 0 and TBL[x-1][y] == 0 and TBL[x+1][y] == 0:
        return "HORIZONTAL"
    # couloir vertical
    if TBL[x+1][y] != 0 and TBL[x-1][y] != 0 and TBL[x][y-1] == 0 and TBL[x][y+1] == 0:
        return "VERTICAL"
    # pas dans un couloir
    return False

# Renvoie la liste des mouvements possibles d'un fantome
def GhostsPossibleMoves(ghost):
    x = ghost[0]
    y = ghost[1]
    dir = ghost[3]

    L = []
    # Détermine les options quand le fantome est dans un couloir vertical
    if isInCorridor(x, y) == "HORIZONTAL":
        if dir == "UP":
            return [(1, 0), (-1, 0)]
        if dir == "DOWN":
            return [(1, 0), (-1, 0)]
        if dir == "LEFT":
            return [(-1, 0)]
        if dir == "RIGHT":
            return [(1, 0)]
        
    # Détermine les options quand le fantome est dans un couloir horizontal
    if isInCorridor(x, y) == "VERTICAL":
        if dir == "UP":
            return [(0, -1)]
        if dir == "DOWN":
            return [(0, 1)]
        if dir == "LEFT":
            return [(0, 1), (0, -1)]
        if dir == "RIGHT":
            return [(0, 1), (0, -1)]
        
    # Si le fantome n'est pas dans un couloir, il choisit arbitrairement dans la mesure du possible
    # Si aucune option n'est envisageable, (qu'il est dans une impasse) il fait demi tour
    else:
        if dir == "UP":
            if ( TBL[x][y-1] != 1 ): L.append((0, -1))
            if ( TBL[x-1][y] != 1 ): L.append((-1, 0))
            if ( TBL[x+1][y] != 1 ): L.append((1, 0))
            if len(L) == 0 and ( TBL[x][y+1] != 1 ): L.append((0, 1))
            return L
        if dir == "DOWN":
            if ( TBL[x][y+1] != 1 ): L.append((0, 1))
            if ( TBL[x-1][y] != 1 ): L.append((-1, 0))
            if ( TBL[x+1][y] != 1 ): L.append((1, 0))
            if len(L) == 0 and ( TBL[x][y-1] != 1 ): L.append((0, -1))
            return L
        if dir == "LEFT":
            if ( TBL[x-1][y] != 1 ): L.append((-1, 0))
            if ( TBL[x][y+1] != 1 ): L.append((0, 1))
            if ( TBL[x][y-1] != 1 ): L.append((0, -1))
            if len(L) == 0 and ( TBL[x+1][y] != 1 ): L.append((1, 0))
            return L
        if dir == "RIGHT":
            if ( TBL[x+1][y] != 1 ): L.append((1, 0))
            if ( TBL[x][y+1] != 1 ): L.append((0, 1))
            if ( TBL[x][y-1] != 1 ): L.append((0, -1))
            if len(L) == 0 and ( TBL[x-1][y] != 1 ): L.append((-1, 0))
            return L

# Renvoie le meilleur mouvement parmi une liste en fonction d'une carte de distances
def GetBestMove(distMap, pos, moves, priority="min"):
    min = math.inf
    bestMove = pos
    x, y = pos

    for move in moves:
        posAfterMove = (x + move[0], y + move[1])
        if distMap[posAfterMove[1]][posAfterMove[0]] < min:
            min = distMap[posAfterMove[1]][posAfterMove[0]]
            bestMove = posAfterMove

    return bestMove

def possibleDirections(weightMap, visitedMap, case):
    directions = []
    x = case["x"]
    y = case["y"]
    dist = case["dist"]
    # Check en bas
    if y < HAUTEUR-1 and weightMap[y+1][x] != math.inf and not visitedMap[y][x]:
        directions.append({
                "x": x,
                "y": y + 1,
                "dist": dist + weightMap[y + 1][x],
            })
    # Check à gauche
    if x > 0 and weightMap[y][x - 1] != math.inf and not visitedMap[y][x]:
        directions.append({
                "x": x - 1,
                "y": y,
                "dist": dist + weightMap[y][x - 1],
            })
    # Check en haut
    if y > 0 and weightMap[y-1][x] != math.inf and not visitedMap[y][x]:
        directions.append({
                "x": x,
                "y": y - 1,
                "dist": dist + weightMap[y - 1][x],
            })
    # Check à droite
    if x < LARGEUR-1 and weightMap[y][x + 1] != math.inf and not visitedMap[y][x]:
        directions.append({
                "x": x + 1,
                "y": y,
                "dist": dist + weightMap[y][x + 1],
            })
    return directions

def checkPaths(initialX, initialY, case, paths, shortestDist, gumMap, weightMap, visitedMap, distMap):
    x = case["x"]
    y = case["y"]
    dist = case["dist"]

    if gumMap[x][y] == 1:
        if dist < distMap[initialY][initialX]:
            distMap[initialY][initialX] = dist
            shortestDist = dist

    elif dist < shortestDist:
        paths += possibleDirections(weightMap, visitedMap, case)

    visitedMap[y][x] = True
    paths.remove(case)
    if len(paths) == 0: return

    for path in paths:
        checkPaths(initialX, initialY, paths[0], paths, shortestDist, gumMap, weightMap, visitedMap, distMap)

def caseDistFromGum(weightMap, visitedMap, gumMap, distMap, x, y):
    shortestDist = math.inf
    visitedMap = generateVisitedMap()
    case = {"x": x, "y": y, "dist": 0}
    paths = [case] + possibleDirections(weightMap, visitedMap, case)
    checkPaths(x, y, case, paths, shortestDist, gumMap, weightMap, visitedMap, distMap)

WEIGHT_MAP = generateWeightMap()

def IAPacman():
    global PacManPos, Ghosts, Score, GUM

    # Génère la carte des distances vers les gums
    distMap = generateDistMap()    
    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            if (WEIGHT_MAP[y][x] != math.inf):
                visitedMap = generateVisitedMap()
                caseDistFromGum(WEIGHT_MAP, visitedMap, GUM, distMap, x, y)

    # Permet d'afficher des informations sur la grille
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            info = distMap[y][x]
            if info == math.inf: info = ""
            SetInfo1(x,y,info)

    # déplacement Pacman
    L = PacManPossibleMoves()
    PacManPos = GetBestMove(distMap, PacManPos, L)

    # Position x du Pac-Man : PacManPos[0]
    # Position y du Pac-Man : PacManPos[1] 
    if GUM[PacManPos[0]][PacManPos[1]] == 1:
        Score += 100
        GUM[PacManPos[0]][PacManPos[1]] = 0

def checkCollisions():
    global PacManState
    for ghost in Ghosts:
        if ghost[0] == PacManPos[0] and ghost[1] == PacManPos[1]:
            if PacManState != "CHASE":
                PacManState = "LOST"
                print(PacManState)

# Déplacement des fantomes
def IAGhosts():
    global Ghosts
    for ghost in Ghosts:
        L = GhostsPossibleMoves(ghost)

        choice = random.randrange(len(L))
        ghost[0] += L[choice][0]
        ghost[1] += L[choice][1]

        # met à jour la direction du fantome
        if (L[choice] == (0, 1)):
            ghost[3] = "DOWN"
        elif (L[choice] == (0, -1)):
            ghost[3] = "UP"
        elif (L[choice] == (-1, 0)):
            ghost[3] = "LEFT"
        elif (L[choice] == (1, 0)):
            ghost[3] = "RIGHT"

# Boucle principale de votre jeu appelée toutes les 500ms
iteration = 0
def PlayOneTurn():
    global iteration

    if not PAUSE_FLAG and PacManState != "LOST" and PacManState != "WON": 
        iteration += 1
        if iteration % 2 == 0 :   IAPacman()
        else:                     IAGhosts()
        checkCollisions()
        
    Affiche(PacmanColor = "yellow", message = "message")  

#endregion

# Démarrage de la fenêtre - ne pas toucher
Window.mainloop()