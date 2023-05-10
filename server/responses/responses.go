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
	ResponseType_USER_REMOVED
)

func writeResponse(connection *net.Conn, response Response) error {
	resp, err := json.Marshal(response)
	if err != nil {
		return err
	}

	_, err = (*connection).Write(append(resp, []byte("<END>")...))
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
	Obmaps   map_repository.Obmaps
	Maps     map_repository.Maps
	NPCs     map_repository.NPCs
	Trainers map_repository.Trainers
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

func WriteUserRemovedResponse(connection *net.Conn, userName string) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_USER_REMOVED,
			Body: userName,
		},
	)
}

func WriteMapResponse(connection *net.Conn, position user_repository.Position, users []user_repository.User) error {
	return writeResponse(
		connection,
		Response{
			Type: ResponseType_MAP,
			Body: MapResponse{
				Obmaps:   map_repository.GetObmaps(),
				Maps:     map_repository.GetMaps(),
				NPCs:     map_repository.GetNPCs(),
				Trainers: map_repository.GetTrainers(),
				Position: position,
				Users:    users,
			},
		},
	)
}
