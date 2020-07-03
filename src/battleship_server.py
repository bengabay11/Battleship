import socket
import select
import random

IP = '0.0.0.0'
PORT = 8820
clients_ready_to_play = []


def handle_positions_of_ships(data):
    """The function handle the data that the client send and return the positions of the ships and
     the username of the client"""
    list2 = data.split('$')
    username = list2[1]
    list1 = list2[0].split('*')
    list_of_positions = []
    for position in list1:
            list2 = position.split(',')
            list_of_positions.append(((int(list2[0]), int(list2[1]))))
    return list_of_positions, username


def game(list_players):
    """The function manages a game between two players"""
    first_turn = random.randint(0, 1)
    if first_turn == 0:
        player1 = list_players[0][0]
        positions1 = list_players[0][1]
        username1 = list_players[0][2]
        player2 = list_players[1][0]
        positions2 = list_players[1][1]
        username2 = list_players[1][2]
    if first_turn == 1:
        player2 = list_players[0][0]
        positions2 = list_players[0][1]
        username2 = list_players[0][2]
        player1 = list_players[1][0]
        positions1 = list_players[1][1]
        username1 = list_players[1][2]
    print username1 + ':'
    print positions1
    print username2 + ':'
    print positions2
    player1.send(username2 + '$' + "first")
    player2.send(username1 + '$' + "second")
    turn = 1
    counter1 = 5
    counter2 = 5
    while counter1 > 0 and counter2 > 0:
        if turn == 1:
            target_position = player1.recv(1024)
            if target_position == '':
                clients_ready_to_play.remove(player1)
                print 'closing connection with ' + username1 + '...'
            else:
                list_target_position = target_position.split(',')
                target_position = (int(list_target_position[0]), int(list_target_position[1]))
                print "target accepted from player1: " + str(target_position)
                if target_position in positions2:
                    print 'sending success'
                    player1.send("success")
                    player2.send(list_target_position[0] + ',' + list_target_position[1] + ',' + 'success')
                    counter2 -= 1
                else:
                    turn = 2
                    print 'sending fail'
                    player1.send("fail")
                    player2.send(list_target_position[0] + ',' + list_target_position[1] + ',' + 'fail')
        else:
            target_position = player2.recv(1024)
            if target_position == '':
                clients_ready_to_play.remove(player2)
                print 'closing connection with ' + username2 + '...'
            else:
                list_target_position = target_position.split(',')
                target_position = (int(list_target_position[0]), int(list_target_position[1]))
                print "target accepted from player2: " + str(target_position)
                if target_position in positions1:
                    print 'sending success'
                    player2.send("success")
                    player1.send(list_target_position[0] + ',' + list_target_position[1] + ',' + 'success')
                    counter1 -= 1
                else:
                    turn = 1
                    print 'sending fail'
                    player2.send("fail")
                    player1.send(list_target_position[0] + ',' + list_target_position[1] + ',' + 'fail')


def main():
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(5)
    open_client_sockets = []
    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                (new_socket, address) = server_socket.accept()
                open_client_sockets.append(new_socket)
            else:
                print 'New data from client!'
                data = current_socket.recv(1024)
                if data == "":
                    open_client_sockets.remove(current_socket)
                    print "Connection with client closed."
                else:
                    global clients_ready_to_play
                    list_positions, username = handle_positions_of_ships(data)
                    clients_ready_to_play.append([current_socket, list_positions, username])
                    if len(clients_ready_to_play) == 2:
                        game(clients_ready_to_play)
                        clients_ready_to_play = []


if __name__ == '__main__':
    main()