package pokete

import (
    "context"
    "log"
    "net"

    "github.com/lxgr-linux/pokete/server/bs_rpc"
    "github.com/lxgr-linux/pokete/server/pokete/msg"
)

func (p Pokete) Start() error {
    socketHost := p.config.ServerHost + ":" + p.config.ServerPort
    server, err := net.Listen("tcp", socketHost)
    if err != nil {
        return err
    }
    defer server.Close()
    log.Printf("Server Running on %s...\n", socketHost)

    reg, err := msg.GetRegistry()
    if err != nil {
        return err
    }

    for {
        connection, err := server.Accept()
        if err != nil {
            return err
        }
        bsRpcClient := bs_rpc.NewClient(connection, *reg)

        log.Print("client connected")
        go func() {
            err := bsRpcClient.Listen(context.Background())
            if err != nil {
                log.Printf("Connection failed, %s", err)
            }
        }()
    }
}

/*
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
*/
