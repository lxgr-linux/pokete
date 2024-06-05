package position

import (
    "context"
    "errors"
    "fmt"
    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    pctx "github.com/lxgr-linux/pokete/server/context"
    error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
    "github.com/lxgr-linux/pokete/server/pokete/user"
)

const UpdateType msg.Type = "pokete.position.update"

type Update struct {
    msg.BaseMsg
    user.User
}

func (u Update) GetType() msg.Type {
    return UpdateType
}

func (u Update) CallForResponse(ctx context.Context) (msg.Body, error) {
    us, _ := pctx.UsersFromContext(ctx)
    conId, _ := pctx.ConnectionIdFromContext(ctx)

    err := us.SetNewPositionToUser(conId, u.Position)
    if errors.Is(err, user.POSITION_ERROR) {
        return error2.NewPositionUnplausible(u.Position, fmt.Sprint(errors.Unwrap(err))), nil
    }
    return msg.EmptyMsg{}, err
}

func NewUpdate(user user.User) Update {
    return Update{msg.BaseMsg{}, user}
}
