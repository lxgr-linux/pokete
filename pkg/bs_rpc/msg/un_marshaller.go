package msg

import (
	"encoding/json"
)

type UnMarshaller func(b []byte) (Body, error)

func NewGenericUnmarshaller[T Body]() UnMarshaller {
	return func(b []byte) (Body, error) {
		var newMsg Msg[T]
		err := json.Unmarshal(b, &newMsg)
		return newMsg.Body, err
	}
}
