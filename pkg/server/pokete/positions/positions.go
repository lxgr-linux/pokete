package positions

import (
    "errors"
    "github.com/lxgr-linux/pokete/server/pokete/user"

    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    positon "github.com/lxgr-linux/pokete/server/pokete/msg/position"
)

var (
    ALREADY_SUBSCRIBED error = errors.New("already subscribed")
)

type Positions struct {
    subscriptions *map[uint64]msg.Responder
}

func (p Positions) Subscribe(conId uint64, responder msg.Responder) error {
    _, ok := (*p.subscriptions)[conId]

    if !ok {
        return ALREADY_SUBSCRIBED
    }

    (*p.subscriptions)[conId] = responder
    return nil
}

func (p Positions) BroadcastChange(originConId uint64, user user.User) (err error) {
    m := positon.NewUpdate(user)
    for conId, resp := range *p.subscriptions {
        if conId != originConId {
            err = resp(m)
        }
    }
    return err
}

func (p Positions) UnSubscribe(conId uint64) {
    delete(*p.subscriptions, conId)
}

func NewPositions() *Positions {
    var tempSubs = make(map[uint64]msg.Responder)
    return &Positions{
        subscriptions: &tempSubs,
    }
}
