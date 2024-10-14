package msg

import (
	"context"
	"fmt"
	"time"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
)

type TestRequestMsg struct {
	Field1 string
	Field2 string
}

func (t TestRequestMsg) CallForResponse(ctx context.Context) (msg.Body, error) {
	fmt.Println("yes")

	return TestResponseMsg{t.Field1 + t.Field2}, nil
}

func (t TestRequestMsg) CallForResponses(ctx context.Context, r msg.Responder) error {
	return fmt.Errorf("not implemented")
}

func (t TestRequestMsg) GetType() msg.Type {
	return "test.request"
}

type TestResponseMsg struct {
	Field3 string
}

func (t TestResponseMsg) CallForResponse(ctx context.Context) (msg.Body, error) {
	fmt.Println("yes")
	return nil, nil
}

func (t TestResponseMsg) CallForResponses(ctx context.Context, r msg.Responder) error {
	return fmt.Errorf("not implemented")
}

func (t TestResponseMsg) GetType() msg.Type {
	return "test.response"
}

type TestStreamMsg struct {
	Start int
}

func (t TestStreamMsg) CallForResponse(ctx context.Context) (msg.Body, error) {
	return nil, fmt.Errorf("not implemented")
}

func (t TestStreamMsg) CallForResponses(ctx context.Context, r msg.Responder) error {
	for i := 0; i < 10; i++ {
		err := r(TestResponseMsg{fmt.Sprintf("%djaja", t.Start+i)})
		if err != nil {
			return err
		}
		time.Sleep(1 * time.Second)
	}

	return nil
}

func (t TestStreamMsg) GetType() msg.Type {
	return "test.stream"
}

func GetRegistry() (*msg.Registry, error) {
	reg := msg.NewRegistry()

	err := reg.RegisterType(TestRequestMsg{}.GetType(), msg.NewGenericUnmarshaller[TestRequestMsg]())
	if err != nil {
		return nil, err
	}

	err = reg.RegisterType(TestResponseMsg{}.GetType(), msg.NewGenericUnmarshaller[TestResponseMsg]())
	if err != nil {
		return nil, err
	}

	err = reg.RegisterType(TestStreamMsg{}.GetType(), msg.NewGenericUnmarshaller[TestStreamMsg]())
	if err != nil {
		return nil, err
	}

	return &reg, nil
}
