package fight

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	"github.com/lxgr-linux/pokete/server/pokete/user"
)

type Player struct {
	User      *user.User
	Incoming  <-chan msg.Body
	Outgoinng msg.Responder
}

func (p Player) Ready() bool {
	return p.Incoming != nil && p.Outgoinng != nil
}

type Fight struct {
	ID           FightID
	players      [2]*Player
	currPlayerId int
	waitForStart chan bool
	waitForEnd   chan bool
}

func (f *Fight) Players() [2]*Player {
	return f.players
}

func (f *Fight) Attacker() *Player {
	return f.players[f.currPlayerId]
}

func (f *Fight) Defender() *Player {
	return f.players[(f.currPlayerId+1)%2]
}

func (f *Fight) Next() {
	f.currPlayerId = (f.currPlayerId + 1) % 2
}

func (f *Fight) WaitForStart() {
	<-f.waitForStart
}

func (f *Fight) WaitForEnd() {
	<-f.waitForEnd
}

func (f *Fight) End() {
	f.waitForEnd <- true
}

func (f *Fight) CheckReady() {
	for _, p := range f.players {
		if !p.Ready() {
			return
		}
	}
	f.waitForStart <- true
}

func New(playerA *user.User, playerB *user.User) Fight {
	return Fight{
		players: [2]*Player{
			{User: playerA},
			{User: playerB},
		},
		currPlayerId: 0,
		waitForEnd:   make(chan bool),
		waitForStart: make(chan bool),
	}
}
