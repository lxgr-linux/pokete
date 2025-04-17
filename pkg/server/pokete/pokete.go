package pokete

import (
	"github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/options"
	"github.com/lxgr-linux/pokete/server/pokete/fight"
	"github.com/lxgr-linux/pokete/server/pokete/positions"
	"github.com/lxgr-linux/pokete/server/pokete/users"
	"github.com/lxgr-linux/pokete/server/resources"
)

type Pokete struct {
	config    *config.Config
	resources *resources.Resources
	users     *users.Users
	options   *options.Options
	positions *positions.Positions
	fights    *fight.Fights
}

func New(config *config.Config, resources *resources.Resources, opts ...options.Func) (*Pokete, error) {
	o, err := options.FromOptionFuncs(opts...)
	if err != nil {
		return nil, err
	}
	p := positions.NewPositions()
	f := fight.NewFights()

	return &Pokete{
		config:    config,
		resources: resources,
		users:     users.NewUsers(p),
		options:   o,
		positions: p,
		fights:    &f,
	}, nil
}
