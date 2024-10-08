package users

import (
	"errors"

	"github.com/lxgr-linux/pokete/server/pokete/positions"
	"github.com/lxgr-linux/pokete/server/pokete/user"
)

var (
	USER_PRESENT      error = errors.New("newUser already present")
	USER_DOESNT_EXIST error = errors.New("user doesn't exist")
)

type Users struct {
	users     *map[uint64]user.User
	positions *positions.Positions
}

func (u Users) Add(conId uint64, newUser user.User) error {
	for _, us := range *u.users {
		if us.Name == newUser.Name {
			return USER_PRESENT
		}
	}

	(*u.users)[conId] = newUser
	err := u.positions.BroadcastChange(conId, newUser)

	return err
}

func (u Users) Remove(conId uint64) {
	us, ok := (*u.users)[conId]
	if ok {
		_ = u.positions.BroadcastRemoval(conId, us.Name)
	}
	u.positions.UnSubscribe(conId)
	delete(*u.users, conId)
}

func (u Users) GetAllUsers() (retUsers []user.User) {
	for _, us := range *u.users {
		retUsers = append(retUsers, us)
	}
	return
}

func (u Users) GetUserByName(name string) (*user.User, error) {
	for _, us := range *u.users {
		if us.Name == name {
			return &us, nil
		}
	}
	return nil, USER_DOESNT_EXIST
}

func (u Users) GetUserByConId(conId uint64) (*user.User, error) {
	us, ok := (*u.users)[conId]
	if !ok {
		return nil, USER_DOESNT_EXIST
	}
	return &us, nil
}

func (u Users) GetAllUserNames() (names []string) {
	for _, us := range *u.users {
		names = append(names, us.Name)
	}
	return
}

func (u Users) SetNewPositionToUser(conId uint64, newPosition user.Position) error {
	us := (*u.users)[conId]
	err := us.Position.Change(newPosition)
	(*u.users)[conId] = us
	err = u.positions.BroadcastChange(conId, us)
	return err
}

func NewUsers(positions2 *positions.Positions) *Users {
	var tempUsers = make(map[uint64]user.User)
	return &Users{
		users:     &tempUsers,
		positions: positions2,
	}
}
