package msg

import (
    "context"
)

const (
    METHOD_CALL_FOR_RESPONSE  = "call_for_response"
    METHOD_CALL_FOR_RESPONSES = "call_for_responses"
    METHOD_RESPONSE_CLOSE     = "response close"
    METHOD_RESPONSE           = "response"
)

type SendClient interface {
    Send(body Body) error
}

type Responder func(body Body) error

type Type string
type Method string

type Body interface {
    CallForResponse(ctx context.Context) (Body, error)
    CallForResponses(ctx context.Context, r Responder) error
    GetType() Type
}

type Msg[T Body] struct {
    Type   Type   `json:"type"`
    Method Method `json:"method"`
    Call   uint32 `json:"call"`
    Body   T      `json:"body"`
}

func NewMsg[T Body](b T, call uint32, method Method) Msg[T] {
    return Msg[T]{b.GetType(), method, call, b}
}
