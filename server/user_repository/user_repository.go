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

func GetByConn(conn *net.Conn) (error, User){
    for _, user := range *users {
        if user.Conn == conn {
            return nil, user
        }
    }
    return fmt.Errorf("user with given connection was not found, somebody fucked up badly"), User{}
}

func RemoveByConn(conn *net.Conn) error {
    err, user := GetByConn(conn); if err != nil {
        return err
    }
    Remove(user.Name)
    return nil
}

func GetAllUsers() (retUsers []User) {
    for _, user := range *users {
        retUsers = append(retUsers, user)
    }
    return 
}

func SetNewPositionToUser(name string, newPosition Position) error {
    user := (*users)[name]
    err := user.Position.Change(newPosition)
    (*users)[name] = user
    return err
}

func GetStartPosition() Position {
	return Position{
		X: 4,
		Y: 4,
	}
}
