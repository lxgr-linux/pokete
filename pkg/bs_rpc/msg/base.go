package msg

import (
    "context"
    "fmt"
)

type BaseMsg struct{}

func (b BaseMsg) CallForResponse(ctx context.Context) (Body, error) {
    return nil, fmt.Errorf("not implemented")
}

func (b BaseMsg) CallForResponses(ctx context.Context, r Responder) error {
    return fmt.Errorf("not implemented")
}

func (b BaseMsg) GetType() Type {
    panic("not implemented")
    return ""
}
