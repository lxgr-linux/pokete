package player

import (
	"context"

	"log/slog"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	pctx "github.com/lxgr-linux/pokete/server/context"
	error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
)

const GetType msg.Type = "pokete.player.get"

type Get struct {
	msg.BaseMsg
	Name string `json:"name"`
}

func (g Get) CallForResponse(ctx context.Context) (msg.Body, error) {
	us, _ := pctx.UsersFromContext(ctx)

	slog.InfoContext(ctx, "rceived user request")

	user, err := us.GetUserByName(g.Name)
	if err != nil {
		return error2.NewUserDoesntExist(), nil
	}

	slog.InfoContext(ctx, "sending player")
	return NewPlayer(*user), nil
}

func (g Get) GetType() msg.Type {
	return GetType
}

func NewGet(name string) Get {
	return Get{msg.BaseMsg{}, name}
}
