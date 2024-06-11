package pokete

import (
	"log"
	"net"

	"github.com/lxgr-linux/pokete/server/context"

	"github.com/lxgr-linux/pokete/bs_rpc"
	"github.com/lxgr-linux/pokete/server/pokete/msg"
)

func (p Pokete) Start() error {
	socketHost := p.config.ServerHost + ":" + p.config.ServerPort
	server, err := net.Listen("tcp", socketHost)
	if err != nil {
		return err
	}
	defer server.Close()
	log.Printf("Server Running on %s...\n", socketHost)

	reg, err := msg.GetRegistry()
	if err != nil {
		return err
	}

	for conId := uint64(0); true; conId++ {
		connection, err := server.Accept()
		if err != nil {
			return err
		}

		bsRpcClient := bs_rpc.NewClient(connection, *reg)
		ctx := context.PoketeContext(p.users, p.resources, p.config, &bsRpcClient, conId, p.positions, p.options)

		go func() {
			log.Println("Client connected")
			defer connection.Close()
			err := bsRpcClient.Listen(ctx)
			p.users.Remove(conId)
			if err != nil {
				log.Printf("Connection failed, %s\n", err)
			} else {
				log.Println("Client disconnected")
			}
		}()
	}

	return nil
}
