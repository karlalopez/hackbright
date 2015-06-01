import socket

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('', 5000))
print "Web server running..."
server_sock.listen(10)

while True:
    client_sock, addr = server_sock.accept()
    print 'We have opened a socket!'
    #print client_sock.recv(100)  # these are the incoming headers
    response = (client_sock.recv(100)).split()
    address = response[1]
    print address

    if address.startswith('/kittens'):
        output = '<h1> Hello Kittens!</h1> <img src="https://www.math.ku.edu/~wsanders/Kittens/new%20kittens/Cute-little-kittens-550x365.jpg"> <br>'
        question_mark = address.find("?")

        if question_mark >= 0:
            query = address[(question_mark+1):len(address)]
            query = query.split("&")
            print query
            number = ""
            text = ""
            for argument in query:
                action = argument.split("=")
                print action
                for argument in action:
                    print action[0]
                    print action[1]
                    if action[0] == "number":
                        number = int(action[1])
                        print number
                    if action[0] == "type":
                        text = action[1]
                        print text
                if number != "":
                    for x in range(number):
                        output = output+" "+str(text)

        client_sock.send("HTTP/1.1 200 OK\n")

    elif address == '/':
        output = '<h1> Hello Cient!</h1>'
        client_sock.send("HTTP/1.1 200 OK\n")

    else:
        output = '<h1>Not found! 404</h1>'
        client_sock.send("HTTP/1.1 404 Not Found\n")

    client_sock.send("Content length: "+str(len(output)))
    client_sock.send("Content-Type: text/html\n\n")

    client_sock.send(output)
    client_sock.close()
