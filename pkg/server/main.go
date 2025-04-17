package main

import (
	_ "embed"
	"io"
	"log"
	"os"
	"path/filepath"

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
	os.MkdirAll(getLogfileDir(), os.ModeDir|os.ModePerm)
	f, err := os.OpenFile(getLogfileDir()+"/pokete_server.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	log.SetOutput(io.MultiWriter(f, os.Stdout))

	p, err := buildPokete()
	if err != nil {
		log.Panic(err)
	}
	err = p.Start()
	if err != nil {
		log.Panic(err)
	}
}

func getLogfileDir() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(config.GetEnvWithFallBack("XDG_DATA_HOME", home+"/.local/share"), "/pokete/")
}

func buildPokete() (*pokete.Pokete, error) {
	cfg := config.FromEnv()

	r, err := resources.FromBytes(assetBytes, baseAssetBytes)
	if err != nil {
		return nil, err
	}

	return pokete.New(&cfg, r, options.WithGreeting("Welcome to the server"))
}
