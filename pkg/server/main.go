package main

import (
	"log"

	"github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/options"
	"github.com/lxgr-linux/pokete/server/pokete"
	"github.com/lxgr-linux/pokete/server/resources"
)

func main() {
	p, err := buildPokete()
	if err != nil {
		log.Panic(err)
	}
	err = p.Start()
	if err != nil {
		log.Panic(err)
	}
}

func buildPokete() (*pokete.Pokete, error) {
	cfg := config.FromEnv()

	r, err := resources.FromDir("./res")
	if err != nil {
		return nil, err
	}

	return pokete.New(&cfg, r, options.WithGreeting("Welcome to the server"))
}
