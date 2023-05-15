package requests

import (
	"fmt"
	"net"

	"github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/provider"
	"github.com/lxgr-linux/pokete/server/responses"
	"github.com/lxgr-linux/pokete/server/user_repository"
)

type RequestType int32

const (
	RequestType_POSITION_UPDATE RequestType = iota
	RequestType_HANDSHAKE
)

type RequestBody interface {
	Handle(connection *net.Conn, p provider.Provider) error
}

type Request[T RequestBody] struct {
	Type RequestType
	Body T
}

type RequestPosition struct {
	user_repository.Position
}

func (r RequestPosition) Handle(connection *net.Conn, p provider.Provider) error {
	users := p.UserRepo.GetAllUsers()
	thisUser, err := p.UserRepo.GetByConn(connection)
	if err != nil {
		return err
	}
	err = p.UserRepo.SetNewPositionToUser(thisUser.Name, r.Position)
	if err != nil {
		err = responses.WritePositionImplausibleResponse(connection, err.Error())
		if err != nil {
			return err
		}
		return fmt.Errorf("connection closed")
	}
	thisUser, err = p.UserRepo.GetByConn(connection)
	if err != nil {
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

func (r RequestHandshake) Handle(connection *net.Conn, p provider.Provider) error {
	position := getStartPosition(p.Config)
	users := p.UserRepo.GetAllUsers()
	newUser := user_repository.User{
		Name:     r.UserName,
		Conn:     connection,
		Position: position,
	}

	if r.Version != p.Config.ClientVersion {
		err := responses.WriteVersionMismatchResponse(connection, p.Config)
		if err != nil {
			return err
		}
		return fmt.Errorf("connection closed")
	}

	err := p.UserRepo.Add(newUser)

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

	err = responses.WriteMapResponse(connection, position, users, p.MapRepo, p.GreetingText)
	if err != nil {
		return err
	}

	return nil
}

func getStartPosition(cfg config.Config) user_repository.Position {
	return user_repository.Position{
		Map: cfg.EntryMap,
		X:   2,
		Y:   9,
	}
}
