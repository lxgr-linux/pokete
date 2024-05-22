package main

import (
    "log"

    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/pokete"
    "github.com/lxgr-linux/pokete/server/resources"
)

func main() {
    p, err := buildPokete()
    if err != nil {
        log.Panic(err)
    }
    p.Start()
}

func buildPokete() (*pokete.Pokete, error) {
    cfg := config.NewConfiFromEnv()

    r, err := resources.FromDir("./res")
    if err != nil {
        return nil, err
    }

    return pokete.New(&cfg, r, pokete.WithGreeting("Welcome to the server"))
}
