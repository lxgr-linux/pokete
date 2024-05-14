package bs_rpc

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
    "io"
    "time"
)

var (
    endSection = []byte("<END>")
)

func NewClient(rw io.ReadWriter, registry msg.Registry) Client {
    calls := make(map[uint32]*[]msg.Body)
    return Client{rw, registry, &calls}
}

type Client struct {
    rw       io.ReadWriter
    registry msg.Registry
    calls    *map[uint32]*[]msg.Body
}

func (c Client) CallForResponse(body msg.Body) (msg.Body, error) {
    callId := uint32(time.Now().Unix())
    err := c.send(body, callId, msg.METHOD_CALL_FOR_RESPONSE)
    if err != nil {
        return nil, err
    }

    var call []msg.Body

    (*c.calls)[callId] = &call

    for {
        if len(call) != 0 {
            ret := call[0]
            delete(*c.calls, callId)
            return ret, nil
        }
    }
}

func (c Client) send(body msg.Body, call uint32, method msg.Method) error {
    m := msg.NewMsg(body, call, method)

    resp, err := json.Marshal(m)
    if err != nil {
        return err
    }

    _, err = c.rw.Write(append(resp, endSection...))
    return err
}

func (c Client) Listen(ctx context.Context) error {
    var msgBuf []byte
    for {
        buf := make([]byte, 32)
        mLen, err := c.rw.Read(buf)
        if err == io.EOF {
            return nil
        }
        if err != nil {
            return err
        }

        if bytes.Contains(buf[:mLen], endSection) {
            msgParts := bytes.Split(buf[:mLen], endSection)

            m, err := Unmarshall(
                &c.registry,
                append(msgBuf, msgParts[0]...),
            )
            if err != nil {
                return err
            }

            switch m.Method {
            case msg.METHOD_RESPONSE:
                call, found := (*c.calls)[m.Call]
                if !found {
                    return fmt.Errorf("call id for response not found")
                }

                *call = append(*call, m.Body)
            case msg.METHOD_CALL_FOR_RESPONSE:
                resp, err := m.Body.CallForResponse(ctx)
                if err != nil {
                    return err
                }
                err = c.send(resp, m.Call, msg.METHOD_RESPONSE)
                if err != nil {
                    return err
                }
            }

            msgBuf = msgParts[1]
        } else {
            msgBuf = append(msgBuf, buf[:mLen]...)
        }
    }
}
