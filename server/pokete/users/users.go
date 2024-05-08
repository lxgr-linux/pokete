package users

import (
	"fmt"
	"net"
)

type Users struct {
	users *map[string]User
}

func (u Users) Add(user User) error {
	for name, _ := range *u.users {
		if name == user.Name {
			return fmt.Errorf("user already present")
		}
	}

	(*u.users)[user.Name] = user

	return nil
}

func (u Users) Remove(name string) {
	delete(*u.users, name)
}

func (u Users) GetByConn(conn *net.Conn) (User, error) {
	for _, user := range *u.users {
		if user.Conn == conn {
			return user, nil
		}
	}
	return User{}, fmt.Errorf("user with given connection was not found, somebody fucked up badly")
}

func (u Users) RemoveByConn(conn *net.Conn) error {
	user, err := u.GetByConn(conn)
	if err != nil {
		return err
	}
	u.Remove(user.Name)
	return nil
}

func (u Users) GetAllUsers() (retUsers []User) {
	for _, user := range *u.users {
		retUsers = append(retUsers, user)
	}
	return
}

func (u Users) GetAllUserNames() (names []string) {
	for _, user := range *u.users {
		names = append(names, user.Name)
	}
	return
}

func (u Users) SetNewPositionToUser(name string, newPosition Position) error {
	user := (*u.users)[name]
	err := user.Position.Change(newPosition)
	(*u.users)[name] = user
	return err
}

func NewUsers() *Users {
	var tempUsers = make(map[string]User)
	return &Users{
		users: &tempUsers,
	}
}
