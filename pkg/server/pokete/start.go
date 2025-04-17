package pokete

import (
	"log/slog"
	"net"

	"github.com/lxgr-linux/pokete/bs_rpc"
	"github.com/lxgr-linux/pokete/server/context"
	"github.com/lxgr-linux/pokete/server/pokete/msg"
)

func (p Pokete) Start() error {
	defaultLogger := slog.Default()
	*defaultLogger = *slog.New(&context.ContextHandler{Handler: defaultLogger.Handler()})

	socketHost := p.config.ServerHost + ":" + p.config.ServerPort
	server, err := net.Listen("tcp", socketHost)
	if err != nil {
		return err
	}
	defer server.Close()
	slog.Info("Server Running", slog.String("socket", socketHost))

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
		ctx := context.PoketeContext(p.users, p.resources, p.fights, p.config, &bsRpcClient, conId, p.positions, p.options)

		go func() {
			slog.InfoContext(ctx, "Client connected")
			defer connection.Close()
			err := bsRpcClient.Listen(ctx)
			p.users.Remove(conId)
			if err != nil {
				slog.ErrorContext(ctx, "Connection failed", slog.Any("error", err))
			} else {
				slog.InfoContext(ctx, "Client disconnected")
			}
		}()
	}

	return nil
}
