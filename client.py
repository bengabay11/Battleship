import socket
import pygame
import ship
import select
from threading import Thread
import time

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 514
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PINK = (255, 20, 147)
YELLOW = (255, 255, 0)
REFRESH_RATE = 60
LEFT = 1
SCROLL = 2
RIGHT = 3
IP = '127.0.0.1'
PORT = 8820
CHARS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'space']
USERNAME = ''
USERNAME2 = ''
TURN = ''
HIT = ''
RIVAL_POSITION = ''
POSITIONS_OF_SHIPS = []
FINISH_GAME = False
FINISH_PUT_SHIPS = False
BEGIN_GAME = False
SEND_POSITION = False
FINISH_CURRENT_GAME = False
SEND_POSITIONS = False
MY_TARGET = ''
SCORE = 0
GAMES = 0


def score(screen):
    """The function presents the score of the player"""
    img = pygame.image.load('base.jpg')
    screen.blit(img, (0, 0))
    pygame.display.flip()
    finish = False
    text1 = pygame.font.SysFont("monospace", 30)
    label = text1.render("SCORE: " + str(SCORE) + '/' + str(GAMES), 1, WHITE)
    screen.blit(label, (250, 90))
    pygame.display.flip()
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                (width, height) = pygame.mouse.get_pos()
                if 16 < height < 73 and 21 < width < 77:
                    img = pygame.image.load('main.jpg')
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    finish = True
                    break


def instructions(screen):
    """The function print image of instructions on the screen"""
    img = pygame.image.load('instructions.jpg')
    screen.blit(img, (0, 0))
    pygame.display.flip()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                (width, height) = pygame.mouse.get_pos()
                if 16 < height < 73 and 21 < width < 77:
                    img = pygame.image.load('main.jpg')
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    finish = True
                    break


def get_text(screen):
    """The function asks text from the client"""
    global USERNAME
    text1 = pygame.font.SysFont("monospace", 30)
    word = []
    mouse_pos_list = []
    position_key_on_screen = 355
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    word.append(" ")
                if event.key == pygame.K_RETURN:
                    new_word = ""
                    for i in word:
                        new_word += i
                    new_word = new_word.replace("space", '')
                    return new_word
                else:
                    key = pygame.key.name(event.key)
                    if key in CHARS:
                        position_key_on_screen += 20
                        if key == 'space':
                            key = ' '
                        label = text1.render(key, 1, WHITE)
                        screen.blit(label, (position_key_on_screen, 90))
                        pygame.display.flip()
                        word.append(key)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos_list.append(pygame.mouse.get_pos())
                (width, height) = pygame.mouse.get_pos()
                if 16 < height < 73 and 21 < width < 77:
                    img = pygame.image.load('main.jpg')
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    finish = True
                    USERNAME = None
                    break


def get_username(screen):
    """The function gets username from the client by using the function get_text()"""
    img = pygame.image.load('base.jpg')
    screen.blit(img, (0, 0))
    text1 = pygame.font.SysFont("monospace", 30)
    label = text1.render("Enter username: ", 1, WHITE)
    label2 = text1.render("Enter only letters and numbers.", 1, WHITE)
    label3 = text1.render("To delete, go back to the menu", 1, WHITE)
    label4 = text1.render("and type a new user name.", 1, WHITE)
    screen.blit(label, (100, 90))
    screen.blit(label2, (50, 300))
    screen.blit(label3, (50, 330))
    screen.blit(label4, (50, 360))
    pygame.display.flip()
    global USERNAME
    USERNAME = get_text(screen)


def placed_ship(width, height):
    """the function checks if the client put the ship correctly"""
    if (width, height) not in POSITIONS_OF_SHIPS and (width - 30, height - 30) not in POSITIONS_OF_SHIPS \
            and (width - 30, height) not in POSITIONS_OF_SHIPS and (width, height - 30) not in POSITIONS_OF_SHIPS and (
    width + 30,
    height + 30) not in POSITIONS_OF_SHIPS and (width + 30, height) not in POSITIONS_OF_SHIPS and (
    width, height + 30) not in \
            POSITIONS_OF_SHIPS and (width - 30, height + 30) not in POSITIONS_OF_SHIPS and (
    width + 30, height - 30) not in \
            POSITIONS_OF_SHIPS:
        return True
    return False


def create_board(screen):
    """The function draw two boards, and the client put the ships on it"""
    img = pygame.image.load('base.jpg')
    screen.blit(img, (0, 0))
    for i in xrange(11):
        pygame.draw.line(screen, WHITE, [30 * i + 30, 170], [30 * i + 30, 470], 4)
        pygame.draw.line(screen, WHITE, [30, 30 * i + 170], [330, 30 * i + 170], 4)
        pygame.draw.line(screen, WHITE, [30 * i + 370, 170], [30 * i + 370, 470], 4)
        pygame.draw.line(screen, WHITE, [370, 30 * i + 170], [670, 30 * i + 170], 4)
    text1 = pygame.font.SysFont("monospace", 30)
    text2 = pygame.font.SysFont("monospace", 50)
    screen.fill(pygame.Color("black"), (65, 85, 605, 50))
    label1 = text2.render(USERNAME, 1, WHITE)
    label2 = text1.render("Put your ships on the left board!", 1, WHITE)
    screen.blit(label1, (320, 20))
    screen.blit(label2, (70, 90))
    pygame.display.flip()
    mouse_pos_list = []
    finish = False
    ok = False
    counter = 5
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos_list.append(pygame.mouse.get_pos())
                (width, height) = pygame.mouse.get_pos()
                if 170 < height < 470 and 30 < width < 330 and counter > 0:
                    while width % 30 != 0:
                        width -= 1
                    while (height + 10) % 30 != 0:
                        height -= 1
                    if placed_ship(width, height):
                        counter -= 1
                        POSITIONS_OF_SHIPS.append((width, height))
                        ship1 = ship.Ship(width, height)
                        screen.blit(ship1.image, ship1.get_pos())
                        pygame.display.flip()
                if 16 < height < 73 and 21 < width < 77:
                    img = pygame.image.load('main.jpg')
                    screen.blit(img, (0, 0))
                    pygame.display.flip()
                    finish = True
                    break
        if counter == 0:
            global FINISH_PUT_SHIPS, SEND_POSITIONS
            screen.fill(pygame.Color("black"), (65, 85, 605, 50))
            label3 = text1.render("Searching for player...", 1, WHITE)
            screen.blit(label3, (70, 90))
            pygame.display.flip()
            if ok is False:
                SEND_POSITIONS = True
                ok = True
            if USERNAME2 != '':
                my_turn(screen)
                img = pygame.image.load('main.jpg')
                screen.blit(img, (0, 0))
                pygame.display.flip()
                finish = True
                break


def my_turn(screen):
    """The function manage the game between the client and his rival. each player send in his turn position to the
    server. first that hit five ships won the game"""
    global BEGIN_GAME, MY_TARGET, HIT, TURN, RIVAL_POSITION, FINISH_PUT_SHIPS, SEND_POSITION, GAMES, SCORE, USERNAME, \
        USERNAME2, POSITIONS_OF_SHIPS, FINISH_CURRENT_GAME
    text1 = pygame.font.SysFont("monospace", 30)
    for i in reversed(xrange(5)):
        if (len(USERNAME) + len(USERNAME2)) > 6:
            screen.fill(pygame.Color("black"), (65, 80, 605, 55))
            label1 = text1.render(USERNAME + ' VS ' + USERNAME2, 1, WHITE)
            label2 = text1.render('The game begins in(' + str((i + 1)) + ')', 1, WHITE)
            screen.blit(label1, (200, 80))
            screen.blit(label2, (200, 100))
            pygame.display.flip()
        else:
            screen.fill(pygame.Color("black"), (65, 85, 605, 50))
            label1 = text1.render(USERNAME + ' VS ' + USERNAME2 + ', The game begins in(' + str((i + 1)) + ')', 1,
                                  WHITE)
            screen.blit(label1, (70, 90))
            pygame.display.flip()
        time.sleep(1)
    screen.fill(pygame.Color("black"), (65, 80, 605, 55))
    pygame.display.flip()
    FINISH_PUT_SHIPS = False
    finish = False
    BEGIN_GAME = True
    my_counter = 5
    rival_counter = 5
    while not finish:
        if TURN == 'first':
            screen.fill(pygame.Color("black"), (65, 85, 605, 50))
            label1 = text1.render('Your turn', 1, WHITE)
            screen.blit(label1, (70, 90))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    (width, height) = pygame.mouse.get_pos()
                    if 170 < height < 470 and 370 < width < 670:
                        while (width - 10) % 30 != 0:
                            width -= 1
                        while (height + 10) % 30 != 0:
                            height -= 1
                        MY_TARGET = str(width - 340) + ',' + str(height)
                        print 'my target = ' + MY_TARGET
                        while HIT == '':
                            pass
                        if HIT == 'success':
                            img = pygame.image.load('vi.jpg')
                            screen.blit(img, (width, height))
                            pygame.display.flip()
                            HIT = ''
                            MY_TARGET = ''
                            SEND_POSITION = False
                            rival_counter -= 1
                        elif HIT == 'fail':
                            img = pygame.image.load('X.jpg')
                            screen.blit(img, (width, height))
                            pygame.display.flip()
                            TURN = 'second'
                            HIT = ''
                            MY_TARGET = ''
                            SEND_POSITION = False
                            break
                    if 16 < height < 73 and 21 < width < 77:
                        finish = True
                        break
        else:
            screen.fill(pygame.Color("black"), (65, 85, 605, 50))
            label1 = text1.render('Wait for your turn', 1, WHITE)
            screen.blit(label1, (70, 90))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    (width, height) = pygame.mouse.get_pos()
                    if 16 < height < 73 and 21 < width < 77:
                        finish = True
                        break
            if HIT == 'success':
                img = pygame.image.load('bom.jpg')
                img.set_colorkey(WHITE)
                screen.blit(img, RIVAL_POSITION)
                pygame.display.flip()
                HIT = ''
                RIVAL_POSITION = ''
                my_counter -= 1
            elif HIT == 'fail':
                img = pygame.image.load('X.jpg')
                screen.blit(img, RIVAL_POSITION)
                pygame.display.flip()
                TURN = 'first'
                HIT = ''
                RIVAL_POSITION = ''
        if my_counter == 0:
            screen.fill(pygame.Color("black"), (65, 85, 620, 50))
            label1 = text1.render('You lose', 1, WHITE)
            screen.blit(label1, (70, 90))
            pygame.display.flip()
            GAMES += 1
            USERNAME = ''
            USERNAME2 = ''
            POSITIONS_OF_SHIPS = []
            time.sleep(2)
            finish = True
            FINISH_CURRENT_GAME = True
            TURN = ''
        elif rival_counter == 0:
            screen.fill(pygame.Color("black"), (65, 85, 620, 50))
            label1 = text1.render('You won!', 1, WHITE)
            screen.blit(label1, (70, 90))
            pygame.display.flip()
            GAMES += 1
            SCORE += 1
            USERNAME = ''
            USERNAME2 = ''
            POSITIONS_OF_SHIPS = []
            time.sleep(2)
            finish = True
            FINISH_CURRENT_GAME = True
            TURN = ''


def main_game():
    """Function that create the main menu"""
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")
    img = pygame.image.load('main.jpg')
    screen.blit(img, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    mouse_pos_list = []
    pygame.display.flip()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos_list.append(pygame.mouse.get_pos())
                (width, height) = pygame.mouse.get_pos()
                if 291 < width < 397 and 268 < height < 299:
                    get_username(screen)
                    if USERNAME is not None:
                        print USERNAME
                        create_board(screen)
                if 286 < width < 413 and 330 < height < 360:
                    score(screen)
                if 214 < width < 483 and 381 < height < 411:
                    instructions(screen)
                if 316 < width < 380 and 434 < height < 466:
                    finish = True
                    global FINISH_GAME
                    FINISH_GAME = True
                    break
    pygame.quit()


def connect_to_server():
    """The function communicates with the server, sends it locations, and receives the user's name, the client's turn,
    and more important details"""
    global FINISH_PUT_SHIPS, HIT, TURN, RIVAL_POSITION, USERNAME2, SEND_POSITION, FINISH_CURRENT_GAME, SEND_POSITIONS, BEGIN_GAME
    while SEND_POSITIONS is False:
        if FINISH_GAME:
            return 0
    print 'connecting to server...'
    client_socket = socket.socket()
    client_socket.connect((IP, PORT))
    while FINISH_GAME is False:
        rlist, wlist, xlist = select.select([client_socket], [client_socket], [])
        if SEND_POSITIONS is True:
            str_positions = str(POSITIONS_OF_SHIPS).strip('[]')
            str_positions = str_positions.replace(', (', '*(')
            str_positions = str_positions.replace('(', '')
            str_positions = str_positions.replace(')', '')
            str_positions = str_positions.replace(' ', '')
            client_socket = socket.socket()
            client_socket.connect((IP, PORT))
            client_socket.send(str_positions + '$' + USERNAME)
            SEND_POSITIONS = False
            FINISH_PUT_SHIPS = True
        if FINISH_PUT_SHIPS is True:
            if client_socket in rlist:
                data = client_socket.recv(1024)
                if data != '':
                    data = data.split('$')
                    USERNAME2 = data[0]
                    TURN = data[1]
                    FINISH_PUT_SHIPS = False
        if BEGIN_GAME:
            if TURN == 'first':
                if SEND_POSITION is False and MY_TARGET != '':
                    client_socket.send(MY_TARGET)
                    print 'sending: ' + MY_TARGET
                    SEND_POSITION = True
                if client_socket in rlist:
                    data = client_socket.recv(1024)
                    if data != '':
                        HIT = data
                        print 'MY HIT: ' + HIT
            else:
                if client_socket in rlist:
                    data = client_socket.recv(1024)
                    if data != '':
                        print 'got from server: ' + data
                        list_rival_position = data.split(',')
                        HIT = list_rival_position[2]
                        RIVAL_POSITION = (int(list_rival_position[0]), int(list_rival_position[1]))
                        print 'RIVAL HIT: ' + HIT
        if FINISH_CURRENT_GAME is True:
            FINISH_CURRENT_GAME = False


def main():
    t1 = Thread(target=main_game)
    t2 = Thread(target=connect_to_server)
    t1.start()
    t2.start()


if __name__ == '__main__':
    main()
