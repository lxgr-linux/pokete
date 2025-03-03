package error

import (
	"fmt"
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
)

const InvalidPokeType msg.Type = "pokete.error.invalid_poke"

type InvalidPoke struct {
	msg.BaseMsg
	Error string `json:"error"`
}

func (p InvalidPoke) GetType() msg.Type {
	return InvalidPokeType
}

func NewInvalidPoke(err error) InvalidPoke {
	return InvalidPoke{msg.BaseMsg{}, fmt.Sprintf("%s", err)}
}
