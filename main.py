from cmu_graphics import *
import random

def onAppStart(app):
    app.newGame = False
    app.hints = False
    app.xmouse = None
    app.ymouse = None
    app.isClickedInside = False
    app.clickedPiece = None
    app.isDragging = False
    app.win = False
    app.level = 1
    app.stepsPerSecond = 10
    app.stepCounter = 0
    app.gameOverSound = Sound('cmu://785943/29317786/mixkit-arcade-retro-game-over-213.wav')
    app.snapSound = Sound('cmu://785943/30599842/finger-snap-179180.mp3')
    app.colorSet = {'lightCoral', 'salmon' , 'fireBrick', 'gold',
                      'moccasin', 'mediumAquamarine', 'darkCyan', 'forestGreen',
                      'skyBlue', 'lightBlue', 'royalBlue', 'lavender', 'plum', 
                      'mediumPurple', 'orchid', 'darkOrchid', 'lightPink',
                      'chocolate'}
        
    
    app.usedColorSet = set()
    app.autoSolve = False
   
    
    selectPiecesList(app)

            
class Piece:
    
    def __init__(self, coordinatesList, app):
        
        offset = random.randint(-110,110)
        for i in range(len(coordinatesList)):
            coordinatesList[i] += offset
        self.coordinates = coordinatesList
        
        possibleColorSet = app.colorSet - app.usedColorSet
        color = random.choice(sorted(possibleColorSet))
        app.usedColorSet.add(color)
        
        
        self.color = color
        self.clicked = False
        self.centerPoint = self.getCenterPoint()
    

        
    
    def __eq__(self, other):
        
        if self.coordinates == other.coordinates:
            return True
    
    def drawPiece(self, clickedPiece, app):
        app.clickedPiece
        drawPolygon(*self.coordinates, fill = self.color, border= 'orange' if self.clicked else None, 
                    borderWidth = 4)
        
    def clickedInside(self, mouseX, mouseY):
        counter = 0
        # GOING THROUGH EACH PAIR OF COORDINATES --> EACH EDGE
        numPoints = len(self.coordinates)
        for i in range (0, len(self.coordinates), 2):
            x0 = self.coordinates[i%numPoints]
            y0 = self.coordinates[(i+1)%numPoints]
            x1 = self.coordinates[(i+2)%numPoints]
            y1 = self.coordinates[(i+3)%numPoints]
  
            higherY = max(y1, y0)
            lowerY = min(y1, y0)
            higherX = max(x1, x0)
            lowerX = min(x1, x0)

            if (mouseY < higherY and mouseY> lowerY) and (mouseX<lowerX or mouseX<x1-((x1-x0)*(y1-mouseY)/(y1-y0))):
                counter +=1
        if counter %2 == 1:
            return True
    
    def movePiece(self, app):
        
        movingPiece = app.PiecesList[app.clickedPiece]
        dx, dy = mouseX-app.xmouse, mouseY-app.ymouse
        counter = 0
        for i in range(0, len(movingPiece),2):
            movingPiece[i] += dx
            movingPiece[i+1] +=dy
            
    def getCenterPoint(self):
        
        xCoordinatesList = []
        for i in range(0, len(self.coordinates), 2):
            xCoordinatesList.append(self.coordinates[i])
        
        yCoordinatesList = []
        for j in range(1, len(self.coordinates),2):
            yCoordinatesList.append(self.coordinates[j])
        

        
        
        smallestX = min(xCoordinatesList)
        largestX = max(xCoordinatesList)
        
        smallestY = min(yCoordinatesList)
        largestY = max(yCoordinatesList)
        
        rectangleWidth = largestX - smallestX
        rectangleHeight = largestY - smallestY
        
        centerPoint = (smallestX+rectangleWidth/2, smallestY+rectangleHeight/2)
        
        return centerPoint
        

        
class Board:
    
    def __init__(self, boardPieceList):
        self.coordinates = boardPieceList
        self.centerPoint = self.getCenterPoint()
   
    def drawBoardPieces(self, app):
        drawPolygon(*self.coordinates, fill = 'grey', 
                        border = 'black' if app.hints == True else None, opacity = 30 )
        drawPolygon(*self.coordinates, fill = None,
                        border = 'black' if app.hints == True else None)  
    
    def getCenterPoint(self):
        xCoordinatesList = []
        for i in range(0, len(self.coordinates), 2):
            xCoordinatesList.append(self.coordinates[i])
        
        yCoordinatesList = []
        for j in range(1, len(self.coordinates),2):
            yCoordinatesList.append(self.coordinates[j])
        

        
        smallestX = min(xCoordinatesList)
        largestX = max(xCoordinatesList)
        
        smallestY = min(yCoordinatesList)
        largestY = max(yCoordinatesList)
        
        rectangleWidth = largestX - smallestX
        rectangleHeight = largestY - smallestY
        
        centerPoint = (smallestX+rectangleWidth/2, smallestY+rectangleHeight/2)
        
        return centerPoint
        




def selectPiecesList(app):
    
    app.win = False
    app.usedColorSet = set()
    
    if app.level == 1:
        app.PiecesList= [Piece([200,100, 250, 150, 200, 250, 150, 150],app), Piece([150, 150, 200, 250, 150, 250],app),
                        Piece([250, 150, 250, 250, 200, 250],app)]

        app.boardComponentList = [Board([200,100, 250, 150, 200, 250, 150, 150]), Board([150, 150, 200, 250, 150, 250]),
                        Board([250, 150, 250, 250, 200, 250])]
        
    
    
    if app.level == 2:

        app.PiecesList = [Piece([100, 100, 300, 100, 200, 200],app), Piece([300, 100, 300, 200, 250, 250, 250, 150],app),
                            Piece([200, 200, 250, 150, 250, 250],app), Piece([300, 200, 300, 300, 200, 300],app),
                            Piece([200, 200, 250, 250, 200, 300, 150, 250],app), Piece([150, 250, 200, 300, 100, 300],app),
                            Piece([100, 100, 200, 200, 100, 300],app)]
        
        app.boardComponentList = [Board([100, 100, 300, 100, 200, 200]), Board([300, 100, 300, 200, 250, 250, 250, 150]),
                            Board([200, 200, 250, 150, 250, 250]), Board([300, 200, 300, 300, 200, 300]),
                            Board([200, 200, 250, 250, 200, 300, 150, 250]), Board([150, 250, 200, 300, 100, 300]),
                            Board([100, 100, 200, 200, 100, 300])]
    
    if app.level == 3:
        
    
        app.PiecesList = [Piece([100, 200, 200, 100, 200, 200],app), Piece([200, 100, 250, 150, 200, 150],app),
        Piece([200, 150, 250, 150, 250, 200, 200, 200],app), Piece([250, 150, 300, 200, 250, 250],app),
        Piece([250, 200, 250, 250, 200, 300, 200, 250],app), Piece([200, 200, 250, 200, 200, 250],app),
        Piece([100, 200, 200, 200, 200, 300],app)]
        
        app.boardComponentList = [Board([100, 200, 200, 100, 200, 200]), Board([200, 100, 250, 150, 200, 150]),
        Board([200, 150, 250, 150, 250, 200, 200, 200]), Board([250, 150, 300, 200, 250, 250]),
        Board([250, 200, 250, 250, 200, 300, 200, 250]), Board([200, 200, 250, 200, 200, 250]),
        Board([100, 200, 200, 200, 200, 300])]
    
    
def onStep(app):
    if app.win == False:
        app.stepCounter +=1
    
    

    
def redrawAll(app):
    drawRect(0,0, app.width, app.height, fill = 'lightGreen' if app.win == True else None, opacity = 60)
    drawPieces(app)
    drawBoard(app)
    if app.win == True:
        drawLabel(f'YOU WON IN {app.stepCounter//10} SECONDS!', app.width/2, 60, size = 27, bold = True)
        drawLabel('Press any key 1-3 to play again :)', app.width/2, 340, size = 20)
        

        

def drawPieces(app):
    
    pieceCounter = 0
    border = False
    for currpiece in app.PiecesList:
        pieceCounter += 1
        if pieceCounter == app.clickedPiece:
            border = True
        currpiece.drawPiece(app.clickedPiece, app)
    
def drawBoard(app):
    for boardPiece in app.boardComponentList:
        boardPiece.drawBoardPieces(app)

def onKeyPress(app, key):
    if key == '1':
        app.level = 1
        selectPiecesList(app)
        app.win = False
    elif key =='2':
        app.level = 2
        selectPiecesList(app)
        app.win = False
    elif key == '3' or key =='4' or key == '5' or key == '6' or key =='7' or key=='8':
        app.level = 3
        selectPiecesList(app)
        app.win = False
    
    elif key == 'h':
        app.hints = not app.hints
    
        



def onMousePress(app, mouseX, mouseY):
    app.xmouse = mouseX
    app.ymouse = mouseY
    
    pieceNumber = -1
    for piece in app.PiecesList:
        pieceNumber +=1
        if piece.clickedInside(mouseX, mouseY) == True:
            app.isClickedInside = True
            app.clickedPiece = pieceNumber
            
    
    if app.clickedPiece != None:
        movingPiece = app.PiecesList[app.clickedPiece]
        movingPiece.clicked = True
    
    
    
    # movingPiece.clicked= True

def onMouseDrag(app, mouseX, mouseY):
    
    
    if app.isClickedInside:
        
        movingPiece = app.PiecesList[app.clickedPiece]
        movingPiece.clicked = True
        movingPieceCoordinates = movingPiece.coordinates
        dx, dy = mouseX-app.xmouse, mouseY-app.ymouse

        for i in range(0, len(movingPieceCoordinates),2):
            movingPieceCoordinates[i] += dx
            movingPieceCoordinates[i+1] +=dy
        
        cx, cy = movingPiece.centerPoint
        movingPiece.centerPoint = (cx+dx, cy+dy)
        
        app.xmouse = mouseX
        app.ymouse = mouseY
        
        
def onMouseRelease(app, mouseX, mouseY):
    app.isDragging = False
    app.isClickedInside = False
    
    snapFunction(app)
    
    for piece in app.PiecesList:
        piece.clicked = False
    
    app.clickedPiece = None
    
    if winChecker(app) == True:
        app.win = True
        app.gameOverSound.play()
        print('win')
    
def snapFunction(app):
    for movingPiece in app.PiecesList:
        if movingPiece.clicked == True:
            mpcx, mpcy = movingPiece.centerPoint
            
            for boardPiece in app.boardComponentList:
                
                bpcx,bpcy = boardPiece.centerPoint
                
                distance = distanceHelper(mpcx, mpcy, bpcx, bpcy )
                if distance <= 12:

                    movingPieceCoordinates = movingPiece.coordinates
                    
                    dx, dy = bpcx - mpcx, bpcy - mpcy
            
                    for i in range(0, len(movingPieceCoordinates),2):
                        movingPieceCoordinates[i] += dx
                        movingPieceCoordinates[i+1] +=dy
                    
                    cx, cy = movingPiece.centerPoint
                    movingPiece.centerPoint = (cx+dx, cy+dy)
                    app.snapSound.play()


def winChecker(app):
    for i in range(len(app.PiecesList)):
        if app.PiecesList[i] != app.boardComponentList[i]:
            return False
    return True
        

def distanceHelper(x0, y0, x1, y1):
    distance = ((x1-x0)**2 + (y1-y0)**2)**0.5
    return distance
    
def main():
    runApp()

main()
