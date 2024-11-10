package fight

import (
	"context"
	"fmt"
	"log/slog"
	"math/rand"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	pctx "github.com/lxgr-linux/pokete/server/context"
	"github.com/lxgr-linux/pokete/server/pokete/fight"
	error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
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
	fights, _ := pctx.FightsFromContext(ctx)

	slog.InfoContext(ctx, "Received request")

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
		slog.WarnContext(ctx, "error recuiving data")
		return nil, err
	}

	switch resp.GetType() {
	case ResponseType:
		dataResp := resp.(Response)
		f := fight.New(attacker, enemy)
		fights.Add(&f)
		slog.InfoContext(ctx, "Started fight", slog.Any("fight", f))

		go func() {
			if err := startFight(ctx, &f); err != nil {
				slog.ErrorContext(ctx, "Fight crashed up", slog.Any("error", err))
			}
		}()

		return dataResp, nil
	default:
		return nil, fmt.Errorf("something went wrong initialting fight")
	}
}

func startFight(ctx context.Context, f *fight.Fight) error {
	defer f.End()
	if err := connectPlayers(f); err != nil {
		return err
	}

	slog.InfoContext(ctx, "Waiting for fight...")
	f.WaitForStart()
	slog.InfoContext(ctx, "Fight ready")

	starter := NewStarter(f.Attacker().User.Name)
	f.Attacker().Outgoing(starter)
	f.Defender().Outgoing(starter)

	for ; ; f.Next() {
		resp := <-f.Attacker().Incoming
		switch resp.GetType() {
		case FightDecisionType:
			seed := NewSeed(rand.Uint32())
			attackResult := resp.(FightDecision)
			err := f.Attacker().Outgoing(seed)
			if err != nil {
				return err
			}

			err = f.Defender().Outgoing(seed)
			if err != nil {
				return err
			}
			err = f.Defender().Outgoing(attackResult)
			if err != nil {
				return err
			}
		default:
			slog.WarnContext(
				ctx, "Received non attackResult resp in fight",
				slog.Any("resp", resp),
			)
		}
	}

	return nil
}

// connectPlayers sets response channels on players
func connectPlayers(f *fight.Fight) error {
	for _, p := range f.Players() {
		respChan, err := p.User.Client.CallForResponses(NewFight(f.ID))
		if err != nil {
			return err
		}
		p.Incoming = respChan
	}

	return nil
}
