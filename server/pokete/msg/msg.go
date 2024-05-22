package msg

import "github.com/lxgr-linux/pokete/server/bs_rpc/msg"

func GetRegistry() (*msg.Registry, error) {
	reg := msg.NewRegistry()
	err := reg.RegisterType(HandshakeType, msg.NewGenericUnmarshaller[Handshake]())
	if err != nil {
		return nil, err
	}
	return &reg, nil
}
