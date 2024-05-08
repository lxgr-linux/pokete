package bs_rpc

import (
    "encoding/json"
    "fmt"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
)

func newInstance[T msg.Body](_ T) (b msg.Msg[T]) {
    return msg.Msg[T]{}
}

func Unmarshall(reg *msg.Registry, b []byte) (msg.Body, error) {
    genericMsg := msg.Msg[msg.Body]{}
    _ = json.Unmarshal(b, &genericMsg)

    emptyOb, err := reg.GetType(genericMsg.Type)
    if err != nil {
        return nil, err
    }

    newMsg := msg.NewMsg(emptyOb)

    fmt.Printf("%#v", newMsg)
    err = json.Unmarshal(b, &newMsg)
    return newMsg.Body, err
}

func Marshall(m msg.Body) ([]byte, error) {
    nm := msg.NewMsg(m)
    return json.Marshal(nm)
}
