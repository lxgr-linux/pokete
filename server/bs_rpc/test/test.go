package main

import (
    "context"
    "fmt"
    "github.com/lxgr-linux/pokete/server/bs_rpc"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
    "log"
)

type TestMsg struct {
    Field1 string
    Field2 string
}

func (t TestMsg) Handle(ctx context.Context, c msg.SendClient) error {
    fmt.Println("yes")
    return nil
}

func (t TestMsg) GetType() msg.Type {
    return "test.testtype"
}

func main() {
    reg := msg.NewRegistry()

    err := reg.RegisterType(TestMsg{})
    if err != nil {
        log.Fatal(err)
    }

    newMsg := TestMsg{"Gallo", "grrr"}

    b, err := bs_rpc.Marshall(&newMsg)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(string(b))

    nBody, err := bs_rpc.Unmarshall(&reg, b)
    if err != nil {
        log.Fatal(err)
    }

    fmt.Println(nBody.GetType())

}
