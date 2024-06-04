package error

import (
    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/pokete/user"
)

const PositionUnplausibleType msg.Type = "pokete.error.position_unplausible"

type PositionUnplausible struct {
    msg.BaseMsg
    Position user.Position `json:"position"`
    Msg      string        `json:"msg"`
}

func (p PositionUnplausible) GetType() msg.Type {
    return PositionUnplausibleType
}

func NewPositionUnplausible(position user.Position, msg string) PositionUnplausible {
    return PositionUnplausible{Position: position, Msg: msg}
}
