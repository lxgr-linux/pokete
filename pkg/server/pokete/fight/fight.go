package fight

import "github.com/lxgr-linux/pokete/server/pokete/user"

type Fight struct {
	ID      FightID
	playerA *user.User
	playerB *user.User
}

func New(playerA *user.User, playerB *user.User) Fight {
	return Fight{playerA: playerA, playerB: playerB}
}
