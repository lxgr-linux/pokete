package user_repository

import (
	"fmt"
    "net"
    "sync"
)

var users *map[string]User
var once sync.Once

func Init() {
	var tempUsers = make(map[string]User)
	once.Do(func() {
		users = &tempUsers
	})
}

func Add(user User) error {
	for name, _ := range *users {
		if name == user.Name {
			return fmt.Errorf("user already present")
		}
	}

	(*users)[user.Name] = user

	return nil
}

func Remove(name string) {
    delete(*users, name)
}

func RemoveByConn(conn *net.Conn) {
    for name, user := range *users {
        if user.Conn == conn {
            Remove(name)
            break
        }
    }
}

func GetAllUsers() (retUsers []User) {
    for _, user := range *users {
        retUsers = append(retUsers, user)
    }
    return 
}

func GetStartPosition() Position {
	return Position{
		X: 4,
		Y: 4,
	}
}
