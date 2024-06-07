package msg

import (
    "context"
    "fmt"
    "github.com/lxgr-linux/pokete/server/pokete/msg/map_info"

    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/config"
    pctx "github.com/lxgr-linux/pokete/server/context"
    error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
    "github.com/lxgr-linux/pokete/server/pokete/user"
    "github.com/lxgr-linux/pokete/server/pokete/users"
)

const HandshakeType msg.Type = "pokete.handshake"

type Handshake struct {
    msg.BaseMsg
    UserName string `json:"user_name"`
    Version  string `json:"version"`
}

func (h Handshake) GetType() msg.Type {
    return HandshakeType
}

func (h Handshake) CallForResponse(ctx context.Context) (msg.Body, error) {
    cfg, _ := pctx.ConfigFromContext(ctx)
    client, _ := pctx.ClientFromContext(ctx)
    u, _ := pctx.UsersFromContext(ctx)
    conId, _ := pctx.ConnectionIdFromContext(ctx)
    res, _ := pctx.ResourcesFromContext(ctx)
    opts, _ := pctx.OptionsFromContext(ctx)

    position := getStartPosition(cfg)

    newUser := user.User{
        Name:     h.UserName,
        Client:   client,
        Position: position,
    }

    if h.Version != cfg.ClientVersion {
        return error2.NewVersionMismatch(cfg.ClientVersion), fmt.Errorf("connection closed")
    }

    err := u.Add(conId, newUser)
    if err == users.USER_PRESENT {
        return error2.NewUserExists(), fmt.Errorf("connection closed")
    }
    if err != nil {
        return nil, err
    }

    return map_info.NewInfo(res, position, u, opts.GreetingText), nil
}

func getStartPosition(cfg *config.Config) user.Position {
    return user.Position{
        Map: cfg.EntryMap,
        X:   2,
        Y:   9,
    }
}
