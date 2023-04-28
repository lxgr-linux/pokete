package user_repository

import "net"

type User struct {
	Name     string
	Position Position
	Conn     *net.Conn
}

type Position struct {
	X uint64
	Y uint32
}
