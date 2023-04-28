package requests

import (
    "fmt"
    "github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/responses"
	"github.com/lxgr-linux/pokete/server/user_repository"
	"net"
)

type RequestType int32

const (
	RequestType_POSITION_UPDATE RequestType = iota
	RequestType_HANDSHAKE
)

type RequestBody interface {
	Handle(connection *net.Conn) error
}

type Request[T RequestBody] struct {
	Type RequestType
	Body T
}

type RequestPosition struct {
    user_repository.Position
}

func (r RequestPosition) Handle(connection *net.Conn) error {
    users := user_repository.GetAllUsers()
    err, thisUser := user_repository.GetByConn(connection); if err != nil {
        return err
    }
    err = user_repository.SetNewPositionToUser(thisUser.Name, r.Position); if err != nil {
        err = responses.WritePositionImplausibleResponse(connection, err.Error()); if err != nil {
            return err
        }
        return fmt.Errorf("connection closed")
    }
    err, thisUser = user_repository.GetByConn(connection); if err != nil {
        return err
    }
    for _, user := range users {
        if user.Conn != connection {
            err := responses.WritePositionChangeResponse(user.Conn, thisUser)
            if err != nil {
                return err
            }
        }
    }

	return nil
}

type RequestHandshake struct {
	UserName string
	Version  string
}

func (r RequestHandshake) Handle(connection *net.Conn) error {
	position := user_repository.GetStartPosition()
	users := user_repository.GetAllUsers()
	newUser := user_repository.User{
		Name:     r.UserName,
		Conn:     connection,
		Position: position,
	}

	if r.Version != config.Get().ClientVersion {
		err := responses.WriteVersionMismatchResponse(connection)
		if err != nil {
			return err
		}
        return fmt.Errorf("connection closed")
	}

	err := user_repository.Add(newUser)

	if err != nil {
		err = responses.WriteUserAllreadyTakenResponse(connection)
		if err != nil {
			return err
		}
        return fmt.Errorf("connection closed")
	}

	for _, user := range users {
		err = responses.WritePositionChangeResponse(user.Conn, newUser)
		if err != nil {
			return err
		}
	}

	err = responses.WriteMapResponse(connection, position, users)
	if err != nil {
		return err
	}

	return nil
}
