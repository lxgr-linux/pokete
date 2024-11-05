package msg

import (
	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
	"github.com/lxgr-linux/pokete/server/pokete/msg/fight"
	"github.com/lxgr-linux/pokete/server/pokete/msg/map_info"
	"github.com/lxgr-linux/pokete/server/pokete/msg/player"
	"github.com/lxgr-linux/pokete/server/pokete/msg/position"
)

func GetRegistry() (*msg.Registry, error) {
	reg := msg.NewRegistry()
	err := reg.RegisterType(HandshakeType, msg.NewGenericUnmarshaller[Handshake]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(error2.VersionMismatchType, msg.NewGenericUnmarshaller[error2.VersionMismatch]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(error2.UserExistsType, msg.NewGenericUnmarshaller[error2.UserExists]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(error2.UserDoesntExistType, msg.NewGenericUnmarshaller[error2.UserDoesntExist]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(position.SubscribePositonsType, msg.NewGenericUnmarshaller[position.SubscribePositons]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(position.UpdateType, msg.NewGenericUnmarshaller[position.Update]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(error2.PositionUnplausibleType, msg.NewGenericUnmarshaller[error2.PositionUnplausible]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(position.RemoveType, msg.NewGenericUnmarshaller[position.Remove]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(map_info.InfoType, msg.NewGenericUnmarshaller[map_info.Info]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(error2.InvalidPokeType, msg.NewGenericUnmarshaller[error2.InvalidPoke]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(fight.RequestType, msg.NewGenericUnmarshaller[fight.Request]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(fight.ResponseType, msg.NewGenericUnmarshaller[fight.Response]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(fight.FightType, msg.NewGenericUnmarshaller[fight.Fight]())
	if err != nil {
		return nil, err
	}
	err = reg.RegisterType(fight.AttackResultType, msg.NewGenericUnmarshaller[fight.AttackResult]())
	if err != nil {
		return nil, err
	}

	err = reg.RegisterType(player.GetType, msg.NewGenericUnmarshaller[player.Get]())
	if err != nil {
		return nil, err
	}

	err = reg.RegisterType(player.PlayerType, msg.NewGenericUnmarshaller[player.Player]())
	if err != nil {
		return nil, err
	}

	return &reg, nil
}
