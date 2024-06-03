package pokete

import (
    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/pokete/positions"
    "github.com/lxgr-linux/pokete/server/pokete/users"
    "github.com/lxgr-linux/pokete/server/resources"
)

type OptionsFunc func(*options) error

func WithGreeting(greeting string) OptionsFunc {
    return func(o *options) error {
        o.GreetingText = greeting
        return nil
    }
}

type options struct {
    GreetingText string
}

type Pokete struct {
    config    *config.Config
    resources *resources.Resources
    users     *users.Users
    options   *options
    positions *positions.Positions
}

func New(config *config.Config, resources *resources.Resources, opts ...OptionsFunc) (*Pokete, error) {
    o := options{}
    for _, of := range opts {
        err := of(&o)
        if err != nil {
            return nil, err
        }
    }

    p := positions.NewPositions()

    return &Pokete{
        config:    config,
        resources: resources,
        users:     users.NewUsers(p),
        options:   &o,
        positions: p,
    }, nil
}
