package test

import (
	"context"
	"log"
	"net"

	"github.com/lxgr-linux/pokete/bs_rpc"
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	msg1 "github.com/lxgr-linux/pokete/bs_rpc/test/msg"
)

func testClient() (results []msg.Body) {
	con, err := net.Dial("tcp", "localhost:9988")
	if err != nil {
		log.Panic(err)
	}

	reg, err := msg1.GetRegistry()
	if err != nil {
		log.Panic(err)
	}

	c := bs_rpc.NewClient(con, *reg)

	go func() {
		err = c.Listen(context.Background())
		if err != nil {
			log.Panic(err)
		}
	}()

	resp, err := c.CallForResponse(msg1.TestRequestMsg{"abc", "def"})
	if err != nil {
		log.Panic(err)
	}
	results = append(results, resp)

	ch, err := c.CallForResponses(msg1.TestStreamMsg{4})
	if err != nil {
		log.Panic(err)
	}
	for {
		val := <-ch
		if val == nil {
			break
		}
		results = append(results, val)
	}

	return
}
