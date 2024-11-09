package fight

import (
	"context"
	"log/slog"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	pctx "github.com/lxgr-linux/pokete/server/context"
	"github.com/lxgr-linux/pokete/server/pokete/fight"
	error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
)

const FightType msg.Type = "pokete.fight.fight"

type Fight struct {
	msg.BaseMsg
	FightID fight.FightID `json:"fight_id"`
}

func (i Fight) GetType() msg.Type {
	return FightType
}

func (i Fight) CallForResponses(ctx context.Context, r msg.Responder) error {
	u, _ := pctx.UsersFromContext(ctx)
	conId, _ := pctx.ConnectionIdFromContext(ctx)
	fights, _ := pctx.FightsFromContext(ctx)

	slog.InfoContext(ctx, "received fight")

	user, err := u.GetUserByConId(conId)
	if err != nil {
		r(error2.UserDoesntExist{})
		return err
	}

	fight, err := fights.Get(i.FightID)
	if err != nil {
		r(error2.UserDoesntExist{})
		return err
	}

	for _, p := range fight.Players() {
		if p.User.Name == user.Name {
			p.Outgoing = r
			fight.CheckReady()
			fight.WaitForEnd()
			return nil
		}
	}

	r(error2.UserDoesntExist{})

	return nil
}

func NewFight(fightID fight.FightID) Fight {
	return Fight{msg.BaseMsg{}, fightID}
}
