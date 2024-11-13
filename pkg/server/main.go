package main

import (
	_ "embed"
	"log"

	"github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/options"
	"github.com/lxgr-linux/pokete/server/pokete"
	"github.com/lxgr-linux/pokete/server/resources"
)

//go:embed res/base_assets.json
var baseAssetBytes []byte

//go:embed res/assets.json
var assetBytes []byte

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

	r, err := resources.FromBytes(assetBytes, baseAssetBytes)
	if err != nil {
		return nil, err
	}

	return pokete.New(&cfg, r, options.WithGreeting("Welcome to the server"))
}
