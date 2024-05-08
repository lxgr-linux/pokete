package pokete

import (
    "log"
    "net"
)

func (p Pokete) Start() error {
    log.Println("Server Running...")
    server, err := net.Listen("tcp", p.config.ServerHost+":"+p.config.ServerPort)
    if err != nil {
        return err
    }
    defer server.Close()

    for {
        connection, err := server.Accept()
        if err != nil {
            return err
        }

        log.Print("client connected")
        go p.listen(connection)
    }
}

func (p Pokete) listen(connection net.Conn) {
    for {
        buffer := make([]byte, 1024)
        mLen, err := connection.Read(buffer)
        if err != nil {
            log.Print("Error reading:", err)
            break
        }
        err = s.handleRequests(buffer[:mLen], &connection)
        if err != nil {
            log.Print("Error handeling:", err)
            break
        }
    }
    err := s.removeUser(&connection)
    if err != nil {
        log.Print("Error closing:", err)
    }
}
