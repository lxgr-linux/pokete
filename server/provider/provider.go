package provider

import (
    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/map_repository"
    "github.com/lxgr-linux/pokete/server/user_repository"
)

type Provider struct {
    Config   config.Config
    MapRepo  map_repository.MapRepo
    UserRepo user_repository.UserRepo
}