package requests

import (
    "net"
)

type RequestType int32

const (
    RequestType_POSITION_UPDATE RequestType = iota
    RequestType_HANDSHAKE
)

type RequestBody interface {
    Handle(connection *net.Conn, p provider.Provider) error
}

type Request[T RequestBody] struct {
    Type RequestType
    Body T
}
