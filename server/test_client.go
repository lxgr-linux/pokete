package main

import (
    "github.com/lxgr-linux/pokete/server/bs_rpc"
    "github.com/lxgr-linux/pokete/server/pokete/msg"
    "log"
    "net"
)

func main() {
    con, err := net.Dial("tcp", "localhost:9988")
    if err != nil {
        log.Panic(err)
    }

    reg, err := msg.GetRegistry()
    if err != nil {
        log.Panic(err)
    }

    c := bs_rpc.NewClient(con, *reg)
    err = c.Send(msg.Handshake{"jaja", "nh"})
    if err != nil {
        log.Panic(err)
    }
    err = c.Send(msg.Handshake{"jaja", "nh"})
    if err != nil {
        log.Panic(err)
    }
    err = c.Send(msg.Handshake{"jaja", "nh"})
    if err != nil {
        log.Panic(err)
    }
    err = c.Send(msg.Handshake{"jaja", "nh"})
    if err != nil {
        log.Panic(err)
    }

}
