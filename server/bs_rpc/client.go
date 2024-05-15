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
    calls := make(map[uint32]*chan msg.Body)
    return Client{rw, registry, &calls}
}

type Client struct {
    rw       io.ReadWriter
    registry msg.Registry
    calls    *map[uint32]*chan msg.Body
}

func (c Client) CallForResponse(body msg.Body) (msg.Body, error) {
    callId := uint32(time.Now().Unix())
    err := c.send(body, callId, msg.METHOD_CALL_FOR_RESPONSE)
    if err != nil {
        return nil, err
    }
    ch := make(chan msg.Body)

    (*c.calls)[callId] = &ch

    ret := <-ch
    close(ch)
    delete(*c.calls, callId)
    return ret, nil
}

func (c Client) CallForResponses(body msg.Body) (<-chan msg.Body, error) {
    callId := uint32(time.Now().Unix())
    err := c.send(body, callId, msg.METHOD_CALL_FOR_RESPONSES)
    if err != nil {
        return nil, err
    }
    ch := make(chan msg.Body)

    (*c.calls)[callId] = &ch

    return ch, nil
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

        msgBuf = append(msgBuf, buf[:mLen]...)

        if bytes.Contains(msgBuf, endSection) {
            msgParts := bytes.Split(msgBuf, endSection)

            m, err := Unmarshall(
                &c.registry,
                msgParts[0],
            )
            if err != nil {
                return err
            }

            switch m.Method {
            case msg.METHOD_RESPONSE:
                ch, found := (*c.calls)[m.Call]
                if !found {
                    return fmt.Errorf("call id for response not found")
                }

                *ch <- m.Body
            case msg.METHOD_RESPONSE_CLOSE:
                ch, found := (*c.calls)[m.Call]
                if !found {
                    return fmt.Errorf("call id for response not found")
                }

                close(*ch)
                delete(*c.calls, m.Call)
            case msg.METHOD_CALL_FOR_RESPONSES:
                err := m.Body.CallForResponses(ctx, func(body msg.Body) error {
                    return c.send(body, m.Call, msg.METHOD_RESPONSE)
                })
                if err != nil {
                    return err
                }
                err = c.send(msg.EmptyMsg{}, m.Call, msg.METHOD_RESPONSE_CLOSE)
                if err != nil {
                    return err
                }
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

            msgBuf = bytes.Join(msgParts[1:], endSection)
        }
    }
}
