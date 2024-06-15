module github.com/lxgr-linux/pokete/server

go 1.22.3

require (
	github.com/joho/godotenv v1.5.1
	github.com/lxgr-linux/pokete/bs_rpc v0.0.0-00010101000000-000000000000
	gopkg.in/yaml.v3 v3.0.1
)

replace github.com/lxgr-linux/pokete/bs_rpc => ../bs_rpc
