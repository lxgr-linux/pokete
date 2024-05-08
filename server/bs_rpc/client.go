package bs_rpc

import (
    "context"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
    "io"
    "strings"
)

var (
    endSection = "<END>"
)

type Client struct {
    rw       io.ReadWriter
    registry msg.Registry
}

func (c Client) Send(body msg.Body) {

}

func (c Client) Listen(ctx context.Context) error {
    var msgBuf []byte
    for {
        buf := make([]byte, 32)
        mLen, err := c.rw.Read(buf)
        if err != nil {
            return err
        }

        if strings.HasSuffix(string(buf[:mLen]), endSection) {
            msgBuf = []byte{}
        } else {
            msgBuf = append(msgBuf, buf...)
        }
    }
}
