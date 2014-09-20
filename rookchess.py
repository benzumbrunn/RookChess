#! /usr/bin/env/python

# RookChess
# Von Benjamin Zumbrunn 
# Im Rahmen der Maturaarbeit an der Minerva Basel 2013/2014
# http://www.benzumbrunn.ch
# Python-Version: 2.7.3


import sys
import pygame
from pygame.locals import *


FPS = 30 # Frames Pro Sekunde

WINDOWWIDTH = 480 # Breite des Fensters in Pixel
WINDOWHEIGHT = 480 # Hoehe des Fensters in Pixel
BOARDWIDTH = 8 # Breite des Spielfelds in Felder
BOARDHEIGHT = 8 # Hoehe des Spielfelds in Felder

PIECESIZE = 60 # Groesse eines Feldes in Pixel

BGIMG = pygame.image.load('pics/chessboard.png') # Laedt das Hintergrundbild
WELCOME = pygame.image.load('pics/welcome.png') # Laedt die Willkommensschrift
WHITEWINS = pygame.image.load('pics/whitewins.png') # Laedt "Weiss gewinnt!"
BLACKWINS = pygame.image.load('pics/blackwins.png') # Laedt "Schwarz gewinnt!"

#                 R   G	  B
WHITE =         (216,216,216)
BLACK =         ( 39, 39, 39)
HLCOLOR =       (  0,  0,200)


EMPTY = 'empty' # leeres Feld

WHITEPAWN = 'whitepawn' # Weisser Bauer
WHITEPAWNIMG = pygame.image.load('pics/whitepawn.png')
WHITEROOK = 'whiterook' # Weisser Turm
WHITEROOKIMG = pygame.image.load('pics/whiterook.png')
WHITEKNIGHT = 'whiteknight' # Weisser Springer
WHITEKNIGHTIMG = pygame.image.load('pics/whiteknight.png')
WHITEBISHOP = 'whitebishop' # Weisser Laeufer
WHITEBISHOPIMG = pygame.image.load('pics/whitebishop.png')
WHITEQUEEN = 'whitequeen' # Weisse Dame
WHITEQUEENIMG = pygame.image.load('pics/whitequeen.png')
WHITEKING = 'whiteking' # Weisser Koenig
WHITEKINGIMG = pygame.image.load('pics/whiteking.png')
WHITEPIECE = [WHITEPAWN, WHITEROOK, WHITEKNIGHT, WHITEBISHOP, WHITEQUEEN, \
              WHITEKING]

BLACKPAWN = 'blackpawn' # Schwarzer Bauer
BLACKPAWNIMG = pygame.image.load('pics/blackpawn.png')
BLACKROOK = 'blackrook' # Schwarzer Turm
BLACKROOKIMG = pygame.image.load('pics/blackrook.png')
BLACKKNIGHT = 'blackknight' # Schwarzer Springer
BLACKKNIGHTIMG = pygame.image.load('pics/blackknight.png')
BLACKBISHOP = 'blackbishop' # Schwarzer Laeufer
BLACKBISHOPIMG = pygame.image.load('pics/blackbishop.png')
BLACKQUEEN = 'blackqueen' # Schwarze Dame
BLACKQUEENIMG = pygame.image.load('pics/blackqueen.png')
BLACKKING = 'blackking' # Schwarzer Koenig
BLACKKINGIMG = pygame.image.load('pics/blackking.png')
BLACKPIECE = [BLACKPAWN, BLACKROOK, BLACKKNIGHT, BLACKBISHOP, BLACKQUEEN, \
              BLACKKING]


def main():
    global FPSCLOCK, DISPLAYSURF

    pygame.init()

    # Setzt den Titel des Programms
    pygame.display.set_caption('RookChess')

    FPSCLOCK = pygame.time.Clock()

    # Bildet das Fenster im richtigen Format ab
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


    while True:
        welcome_screen()

        if run_game() == False:
            break


def run_game():
    board = get_starting_board()
    turn = 'white'
    
    mousex = 0
    mousey = 0

    boxx = 0
    boxy = 0

    # Naechster Klick ist der erste Klick
    firstclick = True
    secondclick = False


    while True:

        for event in pygame.event.get():

            # Variable fuer die ESC-Taste
            ESCAPE = (event.type == KEYUP and event.key == K_ESCAPE)

            # rookchess beenden
            if event.type == QUIT or ESCAPE:
                quit_game()

            # Aktion bei Mausklick
            elif event.type == MOUSEBUTTONUP:

                # Falls keine Figur ausgewaehlt
                if firstclick == True:

                    mousex, mousey = event.pos
                    boxx, boxy = pixel_to_box(mousex, mousey)
                    selectedpiece = board[boxx][boxy]

                    # Korrekte Auswahl
                    # (Feld ist nicht leer und Figur des Spielers)
                    if selectedpiece != EMPTY \
                            and right_color(turn, selectedpiece):

                        firstclick = False
                        secondclick = True

                # Falls bereits gueltige Figur ausgewaehlt, zweiter Zug
                elif secondclick == True:

                    mousex2, mousey2 = event.pos
                    targetx, targety = pixel_to_box(mousex2, mousey2)
                    targetpiece = board[targetx][targety]

                    # Nicht korrektes Ziel, eigene Figur
                    if right_color(turn, targetpiece):
                        firstclick = True
                        secondclick = False

                    # Korrektes Ziel
                    # (Feld ist leer oder Figur des Gegners)
                    elif (targetpiece == EMPTY \
                          or valid_target(turn, targetpiece)) \
                          and valid_move(boxx, boxy, targetx, \
                          targety, selectedpiece, board):

                        # Ist ein Koenig geschlagen?
                        if board[targetx][targety] == WHITEKING:
                            black_wins()

                        elif board[targetx][targety] == BLACKKING:
                            white_wins()

                        board[boxx][boxy] = EMPTY
                        board[targetx][targety] = selectedpiece

                        firstclick = True
                        secondclick = False
                        
                        # Korrekter Zug, also wechselt die Farbe
                        turn = change_turn(turn)

                        # Wird ein Bauer umgewandelt?
                        board = pawn_to_queen(board, selectedpiece, \
                                              targetx, targety)

                    # Nicht korrektes Ziel, ungueltiger Zug
                    elif valid_move(boxx, boxy, targetx, targety, \
                                    selectedpiece, board) == False:
                        firstclick = True
                        secondclick = False


        # Zeichnet das Schachbrett als Hintergrundbild
        DISPLAYSURF.blit(BGIMG, (0, 0))

        # Zeichnet Rand, solange Figur ausgewaehlt ist
        if secondclick == True:
            highlight_box(boxx, boxy)

        # Zeichnet die Figuren auf das Schachbrett.
        draw_board(board)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def get_starting_board():
    # Zeichnet das Schachbrett in der Startposition
    board = []

    # Bilde die zweidimensionale Struktur des Schachbrettes, wobei
    # alle Felder leer sind (den String 'empty' enthalten)
    for i in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT)


    # Die Position [0][0] befindet sich links oben, was der Schachposition A8
    # am naechsten ist.

    # Startpositionen der schwarzen Figuren
    board[0][0] = BLACKROOK
    board[1][0] = BLACKKNIGHT
    board[2][0] = BLACKBISHOP
    board[3][0] = BLACKQUEEN
    board[4][0] = BLACKKING
    board[5][0] = BLACKBISHOP
    board[6][0] = BLACKKNIGHT
    board[7][0] = BLACKROOK
    board[0][1] = BLACKPAWN
    board[1][1] = BLACKPAWN
    board[2][1] = BLACKPAWN
    board[3][1] = BLACKPAWN
    board[4][1] = BLACKPAWN
    board[5][1] = BLACKPAWN 
    board[6][1] = BLACKPAWN
    board[7][1] = BLACKPAWN

    # Startpositionen der weissen Figuren
    board[0][7] = WHITEROOK
    board[1][7] = WHITEKNIGHT
    board[2][7] = WHITEBISHOP
    board[3][7] = WHITEQUEEN
    board[4][7] = WHITEKING
    board[5][7] = WHITEBISHOP
    board[6][7] = WHITEKNIGHT
    board[7][7] = WHITEROOK
    board[0][6] = WHITEPAWN
    board[1][6] = WHITEPAWN
    board[2][6] = WHITEPAWN
    board[3][6] = WHITEPAWN
    board[4][6] = WHITEPAWN
    board[5][6] = WHITEPAWN
    board[6][6] = WHITEPAWN
    board[7][6] = WHITEPAWN

    return board


def draw_board(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if BLACKPAWN in board[x][y]:
                DISPLAYSURF.blit(BLACKPAWNIMG, (x * PIECESIZE, 
                                                y * PIECESIZE))
            if BLACKQUEEN in board[x][y]:
                DISPLAYSURF.blit(BLACKQUEENIMG, (x * PIECESIZE, 
                                                 y * PIECESIZE))
            if BLACKKING in board[x][y]:
                DISPLAYSURF.blit(BLACKKINGIMG, (x * PIECESIZE, 
                                                y * PIECESIZE))
            if BLACKROOK in board[x][y]:
                DISPLAYSURF.blit(BLACKROOKIMG, (x * PIECESIZE, 
                                                y * PIECESIZE))
            if BLACKKNIGHT in board[x][y]:
                DISPLAYSURF.blit(BLACKKNIGHTIMG, (x * PIECESIZE, 
                                                  y * PIECESIZE))
            if BLACKBISHOP in board[x][y]:
                DISPLAYSURF.blit(BLACKBISHOPIMG, (x * PIECESIZE, 
                                                  y * PIECESIZE))
            if WHITEPAWN in board[x][y]:
                DISPLAYSURF.blit(WHITEPAWNIMG, (x * PIECESIZE, 
                                                y * PIECESIZE))
            if WHITEQUEEN in board[x][y]:
                DISPLAYSURF.blit(WHITEQUEENIMG, (x * PIECESIZE, 
                                                 y * PIECESIZE))
            if WHITEKING in board[x][y]:
                DISPLAYSURF.blit(WHITEKINGIMG, (x * PIECESIZE, 
                                                y * PIECESIZE))
            if WHITEROOK in board[x][y]:
                DISPLAYSURF.blit(WHITEROOKIMG, (x * PIECESIZE, 
                                                y * PIECESIZE))
            if WHITEKNIGHT in board[x][y]:
                DISPLAYSURF.blit(WHITEKNIGHTIMG, (x * PIECESIZE, 
                                                  y * PIECESIZE))
            if WHITEBISHOP in board[x][y]:
                DISPLAYSURF.blit(WHITEBISHOPIMG, (x * PIECESIZE, 
                                                  y * PIECESIZE))


def highlight_box(boxx, boxy):
    # Faerbt die Figur ein, die ausgewaehlt wurde
    left, top = top_left_box_coords(boxx, boxy)

    # Letzter Wert dieser Funktion ist die Breite des Rahmens
    return pygame.draw.rect(DISPLAYSURF, HLCOLOR, \
                     (left, top, PIECESIZE, PIECESIZE), 3)


def top_left_box_coords(boxx, boxy):
    # Von Boardkoorinaten zu Pixelkoordinaten wechseln
    left = boxx * PIECESIZE
    top = boxy * PIECESIZE
    return (left, top)


def pixel_to_box(x, y):
    # von Pixelkoordinaten zu Boardkoordinaten wechseln
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = top_left_box_coords(boxx, boxy)
            boxRect = pygame.Rect(left, top, PIECESIZE, PIECESIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def change_turn(turn):
    # Wechselt den Spieler nach gueltigem Zug
    if turn == 'white':
        turn = 'black'
    elif turn == 'black':
        turn = 'white'
    return turn


def right_color(turn, selectedpiece):
    # Testet, ob die ausgewaehlte Figur der Spielerfarbe entspricht
    if turn == 'white' and selectedpiece in WHITEPIECE:
        return True
    if turn == 'black' and selectedpiece in BLACKPIECE:
        return True


def valid_target(turn, targetpiece):
    if turn == 'white' and targetpiece in BLACKPIECE:
        return True
    if turn == 'black' and targetpiece in WHITEPIECE:
        return True


def valid_move(boxx, boxy, targetx, targety, selectedpiece, board):
    # Retourniert die Variable "validmoves", die alle moeglichen Zuege der
    # ausgewaehlten Spielfigur enthaelt
    if selectedpiece == WHITEPAWN:
        validmove = white_pawn_moves(boxx, boxy, targetx, targety, board)
        return validmove
    elif selectedpiece == BLACKPAWN:
        validmove = black_pawn_moves(boxx, boxy, targetx, targety, board)
        return validmove
    elif selectedpiece[5:] == 'rook':
        validmove = rook_moves(boxx, boxy, targetx, targety, board)
        return validmove
    elif selectedpiece[5:] == 'knight':
        validmove = knight_moves(boxx, boxy, targetx, targety, board)
        return validmove
    elif selectedpiece[5:] == 'bishop':
        validmove = bishop_moves(boxx, boxy, targetx, targety, board)
        return validmove
    elif selectedpiece[5:] == 'queen':
        validmove = queen_moves(boxx, boxy, targetx, targety, board)
        return validmove
    elif selectedpiece[5:] == 'king':
        validmove = king_moves(boxx, boxy, targetx, targety, board)
        return validmove


# Hier sind die Zuege fuer die einzelnen Figuren definiert, die erlaubt sind:

def white_pawn_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die weissen Bauern

    # Normaler Zug, 1 nach vorne auf leeres Feld
    if boxy - targety == 1 and boxx - targetx == 0 \
            and board[targetx][targety] == EMPTY:
        return True

    # Doppelter Zug bei Startposition, 2 nach vorne auf leeres Feld
    elif boxy == 6 and boxy - targety == 2 and boxx - targetx == 0 \
            and board[targetx][targety] == EMPTY \
            and board[boxx][boxy - 1] == EMPTY:
        return True

    # 1 nach vorne und 1 nach links oder rechts, wenn schwarze Figur als Ziel
    elif boxy - targety == 1 and (boxx - targetx == 1 or targetx - boxx == 1) \
            and board[targetx][targety] in BLACKPIECE:
        return True


def black_pawn_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die schwarzen Bauern

    # Normaler Zug, 1 nach vorne auf leeres Feld
    if targety - boxy == 1 and targetx - boxx == 0 \
            and board[targetx][targety] == EMPTY:
        return True

    # Doppelter Zug bei Startposition, 2 nach vorne auf leeres Feld
    elif boxy == 1 and targety - boxy == 2 and targetx - boxx == 0 \
            and board[targetx][targety] == EMPTY \
            and board[boxx][boxy + 1] == EMPTY:
        return True

    # 1 nach vorne und 1 nach links oder rechts, wenn weisse Figur als Ziel
    elif targety - boxy == 1 and (boxx - targetx == 1 or targetx - boxx == 1) \
            and board[targetx][targety] in WHITEPIECE:
        return True


def knight_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die Springer

    # 2 Felder in eine Richtung, 1 Feld zu 90 Grad dieser Richtung
    if abs(targety - boxy) == 2 and abs(targetx - boxx) == 1 \
            or abs(targety - boxy) == 1 and abs(targetx - boxx) == 2:
        return True


def rook_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die Tuerme

    # Pruefung fuer jedes Feld nach RECHTS bis zum Ziel
    if 0 < targetx - boxx < 8 and targety - boxy == 0:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx + i][boxy] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
        # ("if not False in blocking" wuerde "if True in blocking" erzeugen)
            return True

    # Pruefung fuer jedes Feld nach LINKS bis zum Ziel
    elif 0 > targetx - boxx > -8 and targety - boxy == 0:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx - i][boxy] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach UNTEN bis zum Ziel
    elif 0 < targety - boxy < 8 and targetx - boxx == 0:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx][boxy + i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach OBEN bis zum Ziel
    elif 0 > targety - boxy > -8 and targetx - boxx == 0:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx][boxy - i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True


def bishop_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die Laeufer

    # Pruefung fuer jedes Feld nach RECHTS UNTEN bis zum Ziel
    if 0 < targetx - boxx < 8 and 0 < targety - boxy < 8 \
            and (abs(targetx - boxx)) / (float(abs(targety - boxy))) == 1.0:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx + i][boxy + i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach LINKS UNTEN bis zum Ziel
    elif 0 > targetx - boxx > -8 and 0 < targety - boxy < 8 \
            and (abs(targetx - boxx)) / (float(abs(targety - boxy))) == 1.0:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx - i][boxy + i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach RECHTS OBEN bis zum Ziel
    elif 0 < targetx - boxx < 8 and 0 > targety - boxy > -8 \
            and (abs(targetx - boxx)) / (float(abs(targety - boxy))) == 1.0:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx + i][boxy - i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach LINKS OBEN bis zum Ziel
    elif 0 > targetx - boxx > -8 and 0 > targety - boxy > -8 \
            and (abs(targetx - boxx)) / (float(abs(targety - boxy))) == 1.0:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx - i][boxy - i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

def queen_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die Damen
 
    # Pruefung fuer jedes Feld nach RECHTS bis zum Ziel
    if 0 < targetx - boxx < 8 and targety - boxy == 0:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx + i][boxy] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
        # ("if not False in blocking" wuerde "if True in blocking" erzeugen)
            return True

    # Pruefung fuer jedes Feld nach LINKS bis zum Ziel
    elif 0 > targetx - boxx > -8 and targety - boxy == 0:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx - i][boxy] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach UNTEN bis zum Ziel
    elif 0 < targety - boxy < 8 and targetx - boxx == 0:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx][boxy + i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach OBEN bis zum Ziel
    elif 0 > targety - boxy > -8 and targetx - boxx == 0:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx][boxy - i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach RECHTS UNTEN bis zum Ziel
    elif 0 < targetx - boxx < 8 and 0 < targety - boxy < 8 \
            and (abs(targetx - boxx)) / (abs(targety - boxy)) == 1:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx + i][boxy + i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach LINKS UNTEN bis zum Ziel
    elif 0 > targetx - boxx > -8 and 0 < targety - boxy < 8 \
            and (abs(targetx - boxx)) / (abs(targety - boxy)) == 1:
        blocking = []
        for i in range(1, abs(targetx - boxx)):
            if board[boxx - i][boxy + i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach RECHTS OBEN bis zum Ziel
    elif 0 < targetx - boxx < 8 and 0 > targety - boxy > -8 \
            and (abs(targetx - boxx)) / (abs(targety - boxy)) == 1:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx + i][boxy - i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True

    # Pruefung fuer jedes Feld nach LINKS OBEN bis zum Ziel
    elif 0 > targetx - boxx > -8 and 0 > targety - boxy > -8 \
            and (abs(targetx - boxx)) / (abs(targety - boxy)) == 1:
        blocking = []
        for i in range(1, abs(targety - boxy)):
            if board[boxx - i][boxy - i] != EMPTY:
                blocking.append(False)
            else:
                blocking.append(True)

        if False not in blocking:
            return True


def king_moves(boxx, boxy, targetx, targety, board):
    # Zuege fuer die Koenige

    # Einfacher Zug nach vorne oder hinten, mithilfe von absolutem Wert
    if abs(targety - boxy) == 1 and targetx - boxx == 0 \
            or abs(targetx - boxx) == 1 and targety - boxy == 0:
        return True

    # Einfacher Zug diagonal, mithilfe von absolutem Wert
    if abs(targety - boxy) == 1 and abs(targetx - boxx) == 1  \
            or abs(targetx - boxx) == 1 and abs(targety - boxy) == 1:
        return True


def pawn_to_queen(board, selectedpiece, targetx, targety):
    # Tauscht weissen Bauer in weisse Dame um
    if selectedpiece == WHITEPAWN and targety == 0:
        board[targetx][targety] = WHITEQUEEN

    # Tauscht schwarzen Bauer in schwarze Dame um
    elif selectedpiece == BLACKPAWN and targety == 7:
        board[targetx][targety] = BLACKQUEEN

    return board


def white_wins():
    # Screen Weiss gewinnt
    while True:
        for event in pygame.event.get():

            # Variable fuer die ESC-Taste
            ESCAPE = (event.type == KEYUP and event.key == K_ESCAPE)

            # rookchess beenden
            if event.type == QUIT or ESCAPE:
                quit_game()
 
            # Neues Spiel
            if event.type == KEYUP and event.key == K_RETURN:
                run_game()


        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(WHITEWINS, (0, 0))
        pygame.display.update()

def black_wins():
    # Screen Schwarz gewinnt
    while True:
        for event in pygame.event.get():

            # Variable fuer die ESC-Taste
            ESCAPE = (event.type == KEYUP and event.key == K_ESCAPE)

            # rookchess beenden
            if event.type == QUIT or ESCAPE:
                quit_game()

            # Neues Spiel
            if event.type == KEYUP:
                run_game()


        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(BLACKWINS, (0, 0))
        pygame.display.update()


def welcome_screen():
    # Angezeigt bei Start des Programmes
    while True:
        for event in pygame.event.get():

            # Variable fuer die ESC-Taste
            ESCAPE = (event.type == KEYUP and event.key == K_ESCAPE)

            # rookchess beenden
            if event.type == QUIT or ESCAPE:
                quit_game()

            if event.type == KEYUP:
                return run_game()

        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(WELCOME, (0, 0))
        pygame.display.update()


def quit_game():
    # Beendet das Programm
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
