package pokete

import (
    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/pokete/users"
    "github.com/lxgr-linux/pokete/server/resources"
    "os/user"
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
    users     *user.Users
    options   *options
}

func New(config *config.Config, resources *resources.Resources, opts ...OptionsFunc) (*Pokete, error) {
    o := options{}
    for _, of := range opts {
        err := of(&o)
        if err != nil {
            return nil, err
        }
    }

    return &Pokete{
        config:    config,
        resources: resources,
        users:     users.NewUsers(),
        options:   &o,
    }, nil
}
