package msg

import (
    "context"
)

type SendClient interface {
    Send(body Body)
}

type Type string

type Body interface {
    Handle(ctx context.Context, c SendClient) error
    GetType() Type
}

type Msg[T Body] struct {
    Type Type
    Body T
}

func NewMsg[T Body](b T) Msg[T] {
    return Msg[T]{b.GetType(), b}
}
