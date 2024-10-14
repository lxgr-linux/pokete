package fight

import "github.com/lxgr-linux/pokete/bs_rpc/msg"

const AttackResultType msg.Type = "pokete.fight.attackResult"

type Result uint

const (
	Result_Attack Result = iota
	Result_RunAway
	Result_Item
	Result_ChoosePoke
)

type AttackResult struct {
	msg.BaseMsg
	Result Result `json:"result"`
	Attack string `json:"attack"`
	Item   string `json:"item"`
}

func (r AttackResult) GetType() msg.Type {
	return AttackResultType
}
