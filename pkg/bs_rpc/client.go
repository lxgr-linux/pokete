package bs_rpc

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"time"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
)

var (
	ENDSECTION       = []byte("<END>")
	DISCONNECT error = errors.New("eof reached")
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

	_, err = c.rw.Write(append(resp, ENDSECTION...))
	return err
}

func (c Client) getCall(callId uint32) (*chan msg.Body, error) {
	ch, found := (*c.calls)[callId]
	if !found {
		return nil, fmt.Errorf("call id for response not found")
	}
	return ch, nil
}

func (c Client) Listen(ctx context.Context) error {
	var msgBuf []byte
	var errorCh = make(chan error)
	var byteCh = make(chan []byte)
	var msgCh = make(chan msg.Msg[msg.Body])

	go func() {
		for {
			c.handleMsg(ctx, <-msgCh, errorCh)
		}
	}()

	bufReadFn := func() {
		buf := make([]byte, 32)
		mLen, err := c.rw.Read(buf)
		if err == io.EOF {
			errorCh <- DISCONNECT
		}
		if err != nil {
			errorCh <- err
		}

		byteCh <- buf[:mLen]
	}

	for {
		go bufReadFn()

		select {
		case err := <-errorCh:
			if err == DISCONNECT {
				return nil
			}
			if err != nil {
				return err
			}
		case buf := <-byteCh:
			msgBuf = append(msgBuf, buf...)
		}

		if bytes.Contains(msgBuf, ENDSECTION) && !bytes.Equal(msgBuf, ENDSECTION) {
			msgParts := bytes.Split(msgBuf, ENDSECTION)

			m, err := Unmarshall(
				&c.registry,
				msgParts[0],
			)
			if err != nil {
				return err
			}

			msgCh <- m

			if len(msgParts[1]) != 0 {
				msgBuf = bytes.Join(msgParts[1:], ENDSECTION)
			} else {
				msgBuf = []byte{}
			}
		}
	}
}

func (c Client) handleMsg(ctx context.Context, m msg.Msg[msg.Body], errorCh chan error) {
	switch m.Method {
	case msg.METHOD_RESPONSE:
		ch, err := c.getCall(m.Call)
		if err != nil {
			errorCh <- err
			return
		}

		*ch <- m.Body
	case msg.METHOD_RESPONSE_CLOSE:
		ch, err := c.getCall(m.Call)
		if err != nil {
			errorCh <- err
			return
		}

		close(*ch)
		delete(*c.calls, m.Call)
	case msg.METHOD_CALL_FOR_RESPONSES:
		go func() {
			err := m.Body.CallForResponses(ctx, func(body msg.Body) error {
				return c.send(body, m.Call, msg.METHOD_RESPONSE)
			})
			if err != nil {
				errorCh <- err
				return
			}
			err = c.send(msg.EmptyMsg{}, m.Call, msg.METHOD_RESPONSE_CLOSE)
			if err != nil {
				errorCh <- err
				return
			}
		}()
	case msg.METHOD_CALL_FOR_RESPONSE:
		go func() {
			resp, respErr := m.Body.CallForResponse(ctx)
			if resp == nil {
				errorCh <- respErr
				return
			}
			err := c.send(resp, m.Call, msg.METHOD_RESPONSE)
			if err != nil {
				errorCh <- err
				return
			}
			if respErr != nil {
				errorCh <- respErr
				return
			}
		}()
	}
}
