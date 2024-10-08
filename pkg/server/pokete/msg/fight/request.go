package fight

import (
	"context"
	"fmt"
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	pctx "github.com/lxgr-linux/pokete/server/context"
	error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
	"log/slog"
)

const RequestType msg.Type = "pokete.fight.request"

type Request struct {
	msg.BaseMsg
	Name string `json:"name"`
}

func (r Request) GetType() msg.Type {
	return RequestType
}

func NewRequest(name string) Request {
	return Request{msg.BaseMsg{}, name}
}

func (r Request) CallForResponse(ctx context.Context) (msg.Body, error) {
	u, _ := pctx.UsersFromContext(ctx)
	conId, _ := pctx.ConnectionIdFromContext(ctx)

	slog.Info("Received request")

	attacker, err := u.GetUserByConId(conId)
	if err != nil {
		return nil, err
	}

	enemy, err := u.GetUserByName(r.Name)
	if err != nil {
		return error2.NewUserDoesntExist(), nil
	}

	resp, err := enemy.Client.CallForResponse(NewRequest(attacker.Name))
	if err != nil {
		slog.Warn("error recuiving data")
		return nil, err
	}

	switch resp.GetType() {
	case ResponseType:
		dataResp := resp.(Response)
		// Add fight object here
		return dataResp, nil
	default:
		slog.Warn("big uff")
		return nil, fmt.Errorf("something went wrong initialting fight")
	}
}
