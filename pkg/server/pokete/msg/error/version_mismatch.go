package error

import "github.com/lxgr-linux/pokete/bs_rpc/msg"

const VersionMismatchType msg.Type = "pokete.error.version_mismatch"

type VersionMismatch struct {
	msg.BaseMsg
	Version string `json:"version"`
}

func (v VersionMismatch) GetType() msg.Type {
	return VersionMismatchType
}

func NewVersionMismatch(version string) VersionMismatch {
	return VersionMismatch{
		msg.BaseMsg{},
		version,
	}
}
