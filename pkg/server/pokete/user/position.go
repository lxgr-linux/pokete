package user

import (
    "fmt"
    "slices"
)

type Position struct {
    Map string
    X   uint64
    Y   uint32
}

func (p *Position) Change(newPosition Position) error {
    if p.isPlausible(newPosition) {
        p.Map = newPosition.Map
        p.X = newPosition.X
        p.Y = newPosition.Y
        return nil
    }
    return fmt.Errorf("position %v is not plausible to result from %v", newPosition, *p)
}

func (p Position) isPlausible(newPosition Position) bool {
    return p.Map != newPosition.Map || slices.Contains(
        []Position{
            {p.Map, p.X, p.Y + 1},
            {p.Map, p.X, p.Y - 1},
            {p.Map, p.X + 1, p.Y},
            {p.Map, p.X - 1, p.Y},
        },
        newPosition,
    )
}