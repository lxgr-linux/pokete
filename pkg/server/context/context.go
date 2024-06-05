package context

import (
    "context"
    "github.com/lxgr-linux/pokete/bs_rpc"
    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/pokete/user"
    "github.com/lxgr-linux/pokete/server/resources"
)

type Positions interface {
    Subscribe(conId uint64, responder msg.Responder) error
    UnSubscribe(conId uint64)
}

type Users interface {
    Add(conId uint64, newUser user.User) error
    Remove(conId uint64)
    GetAllUsers() (retUsers []user.User)
    GetAllUserNames() (names []string)
    SetNewPositionToUser(conId uint64, newPosition user.Position) error
}

type contextKey uint

const (
    contextKey_users contextKey = iota
    contextKey_resources
    contextKey_config
    contextKey_client
    contextKey_id
    contextKey_positions
)

func PoketeContext(users Users, resources *resources.Resources, config *config.Config, client *bs_rpc.Client, connectionId uint64, positions Positions) context.Context {
    ctx := context.Background()
    ctx = context.WithValue(ctx, contextKey_users, users)
    ctx = context.WithValue(ctx, contextKey_resources, resources)
    ctx = context.WithValue(ctx, contextKey_config, config)
    ctx = context.WithValue(ctx, contextKey_client, client)
    ctx = context.WithValue(ctx, contextKey_id, connectionId)
    ctx = context.WithValue(ctx, contextKey_positions, positions)

    return ctx
}

func UsersFromContext(ctx context.Context) (Users, bool) {
    u, ok := ctx.Value(contextKey_users).(Users)
    return u, ok
}

func ResourcesFromContext(ctx context.Context) (*resources.Resources, bool) {
    r, ok := ctx.Value(contextKey_resources).(*resources.Resources)
    return r, ok
}

func ConfigFromContext(ctx context.Context) (*config.Config, bool) {
    c, ok := ctx.Value(contextKey_config).(*config.Config)
    return c, ok
}

func ClientFromContext(ctx context.Context) (*bs_rpc.Client, bool) {
    c, ok := ctx.Value(contextKey_client).(*bs_rpc.Client)
    return c, ok
}

func ConnectionIdFromContext(ctx context.Context) (uint64, bool) {
    c, ok := ctx.Value(contextKey_id).(uint64)
    return c, ok
}

func PositionsFromContext(ctx context.Context) (Positions, bool) {
    p, ok := ctx.Value(contextKey_positions).(Positions)
    return p, ok
}
