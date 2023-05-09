package main

import (
	"encoding/json"
	"github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/status"
    "github.com/lxgr-linux/pokete/server/user_repository"
    "log"
    "net"
	"os"

	"github.com/lxgr-linux/pokete/server/map_repository"
	"github.com/lxgr-linux/pokete/server/requests"
)

func main() {
	config.Init()
	user_repository.Init()
	err := map_repository.Read()
	if err != nil {
		panic(err.Error())
	}
	log.Print("Server Running...")
	server, err := net.Listen(config.Get().ServerType, config.Get().ServerHost+":"+config.Get().ServerPort)
	if err != nil {
		log.Print("Error listening:", err.Error())
		os.Exit(1)
	}
	defer server.Close()
    go status.HandleRequests()
	log.Print("Listening on " + config.Get().ServerHost + ":" + config.Get().ServerPort)
	log.Print("Waiting for client...")
	for {
		connection, err := server.Accept()
		if err != nil {
			log.Print("Error accepting: ", err.Error())
			os.Exit(1)
		}
		log.Print("client connected")
		go processClient(connection)
	}
}

func unmarshallRequest[T requests.RequestBody](res []byte, genericResponseObject *requests.Request[requests.RequestBody]) error {
	responseObject := requests.Request[T]{}
	err := json.Unmarshal(res, &responseObject)
	if err != nil {
		return err
	}

	genericResponseObject.Body = responseObject.Body

	return nil
}

func handleRequests(res []byte, connection *net.Conn) error {
	genericResponseObject := requests.Request[requests.RequestBody]{}
	err := json.Unmarshal(res, &genericResponseObject)

	switch genericResponseObject.Type {
	case requests.RequestType_POSITION_UPDATE:
		err = unmarshallRequest[requests.RequestPosition](res, &genericResponseObject)
		if err != nil {
			return err
		}
	case requests.RequestType_HANDSHAKE:
		err = unmarshallRequest[requests.RequestHandshake](res, &genericResponseObject)
		if err != nil {
			return err
		}
	}

	log.Printf("%#v\n", genericResponseObject)
	err = genericResponseObject.Body.Handle(connection)
	if err != nil {
		return err
	}
	return nil
}

func processClient(connection net.Conn) {
	for {
		buffer := make([]byte, 1024)
		mLen, err := connection.Read(buffer)
		if err != nil {
			log.Print("Error reading:", err)
			break
		}
		err = handleRequests(buffer[:mLen], &connection)
		if err != nil {
			log.Print("Error handeling:", err.Error())
			break
		}
	}
    _ = user_repository.RemoveByConn(&connection)
    connection.Close()
}
