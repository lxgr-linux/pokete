package requests

import "github.com/lxgr-linux/pokete/server/pokete/users"

type RequestPosition struct {
    users.Position
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
