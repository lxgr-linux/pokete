package msg

import (
    "context"
    "log"

    "github.com/lxgr-linux/pokete/server/bs_rpc/msg"
)

const HandshakeType msg.Type = "pokete.handshake"

type Handshake struct {
    msg.BaseMsg
    UserName string
    Version  string
}

func (h Handshake) GetType() msg.Type {
    return HandshakeType
}

func (h Handshake) Handle(ctx context.Context, c msg.SendClient) error {
    /*position := getStartPosition(p.Config)
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
      }*/

    log.Println("handshake shaken")

    return nil
}
