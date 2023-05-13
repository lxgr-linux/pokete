package server

import (
	"github.com/lxgr-linux/pokete/server/provider"
	"log"
	"net"

	"github.com/lxgr-linux/pokete/server/config"
	"github.com/lxgr-linux/pokete/server/map_repository"
	"github.com/lxgr-linux/pokete/server/requests/handler"
	"github.com/lxgr-linux/pokete/server/responses"
	"github.com/lxgr-linux/pokete/server/status"
	"github.com/lxgr-linux/pokete/server/user_repository"
)

func NewServer(cfg config.Config) (server Server, err error) {
	mapRepo, err := map_repository.NewMapRepo()
	if err != nil {
		return
	}
	return Server{
		provider.Provider{
			Config:   cfg,
			MapRepo:  mapRepo,
			UserRepo: user_repository.NewUserRepo(),
		},
	}, nil
}

type Server struct {
	provider.Provider
}

func (s Server) Start() {
	log.Print("Server Running...")
	server, err := net.Listen(s.Config.ServerType, s.Config.ServerHost+":"+s.Config.ServerPort)
	if err != nil {
		log.Fatal("Error listening:", err.Error())
	}
	defer server.Close()
	go status.NewStatusHandler(s.Provider).HandleRequests()
	log.Print("Listening on " + s.Config.ServerHost + ":" + s.Config.ServerPort)
	log.Print("Waiting for client...")
	for {
		connection, err := server.Accept()
		if err != nil {
			log.Fatal("Error accepting: ", err.Error())
		}
		log.Print("client connected")
		go s.processClient(connection)
	}
}

func (s Server) handleRequests(res []byte, connection *net.Conn) error {
	genericResponseObject, err := handler.Handle(res)
	log.Printf("%#v\n", genericResponseObject)
	err = genericResponseObject.Body.Handle(connection, s.Provider)
	if err != nil {
		return err
	}
	return nil
}

func (s Server) removeUser(connection *net.Conn) error {
	thisUser, err := s.UserRepo.GetByConn(connection)
	err = s.UserRepo.RemoveByConn(connection)
	for _, user := range s.UserRepo.GetAllUsers() {
		err = responses.WriteUserRemovedResponse(user.Conn, thisUser.Name)
	}
	err = (*connection).Close()
	return err
}

func (s Server) processClient(connection net.Conn) {
	for {
		buffer := make([]byte, 1024)
		mLen, err := connection.Read(buffer)
		if err != nil {
			log.Print("Error reading:", err)
			break
		}
		err = s.handleRequests(buffer[:mLen], &connection)
		if err != nil {
			log.Print("Error handeling:", err)
			break
		}
	}
	err := s.removeUser(&connection)
	if err != nil {
		log.Print("Error closing:", err)
	}
}
