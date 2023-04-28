package responses

import (
	"encoding/json"
	"fmt"
	"github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/map_repository"
	"github.com/lxgr-linux/pokete/server/user_repository"
	"net"
)

type ResponseType int32

const (
	ResponseType_MAP ResponseType = iota
	ResponseType_POSITION_CHANGE
	ResponseType_USER_ALLREADY_PRESENT
	ResponseType_VERSION_MISMATCH
	ResponseType_POSITION_IMPLAUSIBLE
)

func writeResponse(connection *net.Conn, response Response) error {
	resp, err := json.Marshal(response)
	if err != nil {
		return err
	}

	_, err = (*connection).Write(resp)
	if err != nil {
		return err
	}
	return nil
}

type Response struct {
	Type ResponseType
	Body any
}

type MapResponse struct {
	Obmap    map_repository.Obmap
	Map      map_repository.Map
	Position user_repository.Position
	Users    []user_repository.User
}

func WritePositionChangeResponse(connection *net.Conn, user user_repository.User) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_POSITION_CHANGE,
			Body: user,
		},
	)
}

func WriteUserAllreadyTakenResponse(connection *net.Conn) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_USER_ALLREADY_PRESENT,
			Body: nil,
		},
	)
}

func WritePositionImplausibleResponse(connection *net.Conn, message string) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_POSITION_IMPLAUSIBLE,
			Body: message,
		},
	)
}

func WriteVersionMismatchResponse(connection *net.Conn) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_VERSION_MISMATCH,
			Body: fmt.Sprintf("Required version is %s", config.Get().ClientVersion),
		},
	)
}

func WriteMapResponse(connection *net.Conn, position user_repository.Position, users []user_repository.User) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_MAP,
			Body: MapResponse{
				Obmap:    map_repository.GetObmap(),
				Map:      map_repository.GetMap(),
				Position: position,
				Users:    users,
			},
		},
	)
}
