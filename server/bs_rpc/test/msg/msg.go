package msg

import (
    "context"
    "fmt"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
)

type TestRequestMsg struct {
    Field1 string
    Field2 string
}

func (t TestRequestMsg) CallForResponse(ctx context.Context) (msg.Body, error) {
    fmt.Println("yes")

    return TestResponseMsg{t.Field1 + t.Field2}, nil
}

func (t TestRequestMsg) GetType() msg.Type {
    return "test.request"
}

type TestResponseMsg struct {
    Field3 string
}

func (t TestResponseMsg) CallForResponse(ctx context.Context) (msg.Body, error) {
    fmt.Println("yes")
    return nil, nil
}

func (t TestResponseMsg) GetType() msg.Type {
    return "test.response"
}

func GetRegistry() (*msg.Registry, error) {
    reg := msg.NewRegistry()

    err := reg.RegisterType(TestRequestMsg{}.GetType(), msg.NewGenericUnmarshaller[TestRequestMsg]())
    if err != nil {
        return nil, err
    }

    err = reg.RegisterType(TestResponseMsg{}.GetType(), msg.NewGenericUnmarshaller[TestResponseMsg]())
    if err != nil {
        return nil, err
    }

    return &reg, nil
}
