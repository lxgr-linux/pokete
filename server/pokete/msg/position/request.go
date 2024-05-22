package msg

import (
    "context"
    "fmt"
    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/pokete/users"
)

const PositionType msg.Type = "pokete.position.request"

type Position struct {
    users.Position
}

func (p Position) GetType() msg.Type {
    return PositionType
}

func (p Position) Handle(ctx context.Context, c msg.SendClient) error {
    /*users := p.UserRepo.GetAllUsers()
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
      }*/

    fmt.Println("postion hit")

    return nil
}
