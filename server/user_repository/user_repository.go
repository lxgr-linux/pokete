package user_repository

import (
	"fmt"
	"net"
)

type UserRepo struct {
	users *map[string]User
}

func (u UserRepo) Add(user User) error {
	for name, _ := range *u.users {
		if name == user.Name {
			return fmt.Errorf("user already present")
		}
	}

	(*u.users)[user.Name] = user

	return nil
}

func (u UserRepo) Remove(name string) {
	delete(*u.users, name)
}

func (u UserRepo) GetByConn(conn *net.Conn) (User, error) {
	for _, user := range *u.users {
		if user.Conn == conn {
			return user, nil
		}
	}
	return User{}, fmt.Errorf("user with given connection was not found, somebody fucked up badly")
}

func (u UserRepo) RemoveByConn(conn *net.Conn) error {
	user, err := u.GetByConn(conn)
	if err != nil {
		return err
	}
	u.Remove(user.Name)
	return nil
}

func (u UserRepo) GetAllUsers() (retUsers []User) {
	for _, user := range *u.users {
		retUsers = append(retUsers, user)
	}
	return
}

func (u UserRepo) GetAllUserNames() (names []string) {
	for _, user := range *u.users {
		names = append(names, user.Name)
	}
	return
}

func (u UserRepo) SetNewPositionToUser(name string, newPosition Position) error {
	user := (*u.users)[name]
	err := user.Position.Change(newPosition)
	(*u.users)[name] = user
	return err
}

func NewUserRepo() UserRepo {
	var tempUsers = make(map[string]User)
	return UserRepo{
		users: &tempUsers,
	}
}
