package msg

import (
    "context"
    "fmt"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/pokete/users"
)

const PositionUpdateType msg.Type = "pokete.position.update"

type Update struct {
    users.User
}

func (u Update) GetType() msg.Type {
    return PositionUpdateType
}

func (u Update) Handle(ctx context.Context, c msg.SendClient) error {

    return fmt.Errorf("not implemented")
}
