package positon

import (
    "context"
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

    return p.Subscribe(conId, r)
}
