package position

import (
	"context"
	"fmt"
	"log/slog"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	pctx "github.com/lxgr-linux/pokete/server/context"
)

const SubscribePositonsType msg.Type = "pokete.position.subscribe"

type SubscribePositons struct {
	msg.BaseMsg
}

func (s SubscribePositons) GetType() msg.Type {
	return SubscribePositonsType
}

func (s SubscribePositons) CallForResponses(ctx context.Context, r msg.Responder) error {
	p, _ := pctx.PositionsFromContext(ctx)
	conId, _ := pctx.ConnectionIdFromContext(ctx)
	slog.InfoContext(ctx, "Subscribe")

	return p.Subscribe(conId, r)
}

func NewSubscribePositions() SubscribePositons {
	return SubscribePositons{msg.BaseMsg{}}
}

func ReveiveUpdates(ctx context.Context) error {
	client, _ := pctx.ClientFromContext(ctx)
	us, _ := pctx.UsersFromContext(ctx)
	conId, _ := pctx.ConnectionIdFromContext(ctx)

	ch, err := client.CallForResponses(NewSubscribePositions())
	if err != nil {
		return err
	}

	for {
		rawU := <-ch
		if rawU == nil {
			break
		}

		u, ok := rawU.(Update)
		if !ok {
			return fmt.Errorf("message not positon update but: `%s`", u.GetType())
		}

		err = us.SetNewPositionToUser(conId, u.Position)
		if err != nil {
			return err
		}
		/*if errors.Is(err, user.POSITION_ERROR) {
		return error2.NewPositionUnplausible(u.Position, fmt.Sprint(errors.Unwrap(err))), nil
		}*/
	}

	return nil
}
