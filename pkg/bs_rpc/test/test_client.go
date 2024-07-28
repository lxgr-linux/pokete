package main

import (
	"context"
	"fmt"
	"log"
	"net"

	"github.com/lxgr-linux/pokete/bs_rpc"
	"github.com/lxgr-linux/pokete/bs_rpc/test/msg"
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

	go func() {
		err = c.Listen(context.Background())
		if err != nil {
			log.Panic(err)
		}
	}()

	resp, err := c.CallForResponse(msg.TestRequestMsg{"abc", "def"})
	if err != nil {
		log.Panic(err)
	}
	fmt.Println(resp)

	ch, err := c.CallForResponses(msg.TestStreamMsg{4})
	if err != nil {
		log.Panic(err)
	}
	for {
		val := <-ch
		if val == nil {
			break
		}
		fmt.Println(val)
	}
}
