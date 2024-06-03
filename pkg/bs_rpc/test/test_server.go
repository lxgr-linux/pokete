package main

import (
    "context"
    "github.com/lxgr-linux/pokete/bs_rpc"
    "github.com/lxgr-linux/pokete/bs_rpc/test/msg"
    "log"
    "net"
)

func main() {
    server, err := net.Listen("tcp", "localhost:9988")
    if err != nil {
        log.Panic(err)
    }
    defer server.Close()

    reg, err := msg.GetRegistry()
    if err != nil {
        log.Panic(err)
    }

    for {
        con, err := server.Accept()
        if err != nil {
            log.Panic(err)
        }

        c := bs_rpc.NewClient(con, *reg)

        err = c.Listen(context.Background())
        if err != nil {
            log.Panic(err)
        }
    }
}
