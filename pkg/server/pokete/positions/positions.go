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

type Subscription struct {
    Responder msg.Responder
    Ch        chan int
}

type Positions struct {
    subscriptions *map[uint64]Subscription
}

func (p Positions) Subscribe(conId uint64, responder msg.Responder) error {
    _, ok := (*p.subscriptions)[conId]

    if ok {
        return ALREADY_SUBSCRIBED
    }

    ch := make(chan int)
    (*p.subscriptions)[conId] = Subscription{responder, ch}
    <-ch
    return nil
}

func (p Positions) broadcast(originConId uint64, body msg.Body) (err error) {
    for conId, sub := range *p.subscriptions {
        if conId != originConId {
            err = sub.Responder(body)
        }
    }
    return err
}

func (p Positions) BroadcastChange(originConId uint64, user user.User) (err error) {
    return p.broadcast(originConId, positon.NewUpdate(user))
}

func (p Positions) BroadcastRemoval(originConId uint64, userName string) (err error) {
    return p.broadcast(originConId, positon.NewRemove(userName))
}

func (p Positions) UnSubscribe(conId uint64) {
    delete(*p.subscriptions, conId)
}

func NewPositions() *Positions {
    var tempSubs = make(map[uint64]Subscription)
    return &Positions{
        subscriptions: &tempSubs,
    }
}
