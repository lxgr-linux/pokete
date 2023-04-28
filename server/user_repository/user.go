package user_repository

import (
    "fmt"
	"net"

	"golang.org/x/exp/slices"
)

type User struct {
	Name     string
	Position Position
	Conn     *net.Conn
}

type Position struct {
	X uint64
	Y uint32
}

func (p *Position) Change(newPosition Position) error {
	if p.isPlausible(newPosition) {
		p.X = newPosition.X
		p.Y = newPosition.Y
		return nil
	}
	return fmt.Errorf("position %v is not playsible to result from %v", newPosition, *p)
}

func (p Position) isPlausible(newPosition Position) bool {
	return slices.Contains(
		[]Position{
			{p.X, p.Y + 1},
			{p.X, p.Y - 1},
			{p.X + 1, p.Y},
			{p.X - 1, p.Y},
		},
		newPosition,
	)
}
