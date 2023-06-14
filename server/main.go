package main

import (
    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/server"
    "log"
)

func main() {
	pokete, err := server.NewServer(config.NewConfiFromEnv())
    if err != nil {
        log.Fatal(err)
    }

    pokete.WithGreetingText("Welcome to the server")

    pokete.Start()
}
