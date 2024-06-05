package msg

import (
    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
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

    return &reg, nil
}
