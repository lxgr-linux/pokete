module github.com/lxgr-linux/pokete/server

go 1.22.3

require (
	github.com/joho/godotenv v1.5.1
	github.com/lxgr-linux/pokete/server/bs_rpc v0.0.0-00010101000000-000000000000
)

replace github.com/lxgr-linux/pokete/server/bs_rpc => ./bs_rpc
