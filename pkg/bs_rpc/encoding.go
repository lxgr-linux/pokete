package bs_rpc

import (
    "encoding/json"

    "github.com/lxgr-linux/pokete/bs_rpc/msg"
)

func Unmarshall(reg *msg.Registry, b []byte) (msg.Msg[msg.Body], error) {
    genericMsg := msg.Msg[msg.Body]{}
    _ = json.Unmarshal(b, &genericMsg)

    unMarshaller, err := reg.GetUnMarshaller(genericMsg.Type)
    if err != nil {
        return genericMsg, err
    }

    body, err := unMarshaller(b)
    genericMsg.Body = body
    return genericMsg, err
}

func Marshall(m msg.Body, call uint32, method msg.Method) ([]byte, error) {
    nm := msg.NewMsg(m, call, method)
    return json.Marshal(nm)
}
