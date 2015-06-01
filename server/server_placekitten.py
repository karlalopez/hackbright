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
        output = '<h1> Hello Kittens!</h1>'
        question_mark = address.find("?")
        if question_mark >= 0:
            query = address[(question_mark+1):len(address)]
            query = query.split("&")
            width = ""
            height = ""
            for argument in query:
                action = argument.split("=")
                print action
                for argument in action:
                    print action[0]
                    print action[1]
                    if action[0] == "width":
                        width = int(action[1])
                        print width
                    if action[0] == "height":
                        height = action[1]
                        print height
            output = output+'<img scr="http://placekitten.com/g/'+str(width)+'/'+str(height)+'">'
            print output
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
