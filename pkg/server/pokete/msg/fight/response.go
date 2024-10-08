package fight

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
)

const ResponseType msg.Type = "pokete.fight.response"

type Response struct {
	msg.BaseMsg
	Accept bool `json:"accept"`
}

func (i Response) GetType() msg.Type {
	return ResponseType
}

func NewResponse(accept bool) Response {
	return Response{msg.BaseMsg{}, accept}
}
