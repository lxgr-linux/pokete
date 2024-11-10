package fight

import "github.com/lxgr-linux/pokete/bs_rpc/msg"

const FightDecisionType msg.Type = "pokete.fight.fightDecision"

type Result uint

const (
	Result_Attack Result = iota
	Result_RunAway
	Result_Item
	Result_ChoosePoke
)

type FightDecision struct {
	msg.BaseMsg
	Result Result `json:"result"`
	Attack string `json:"attack"`
	Item   string `json:"item"`
}

func (r FightDecision) GetType() msg.Type {
	return FightDecisionType
}
