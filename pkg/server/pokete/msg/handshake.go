package msg

import (
    "context"
    "fmt"
    "log"

    "github.com/lxgr-linux/pokete/bs_rpc/msg"
    "github.com/lxgr-linux/pokete/server/config"
    pctx "github.com/lxgr-linux/pokete/server/context"
    error2 "github.com/lxgr-linux/pokete/server/pokete/msg/error"
    "github.com/lxgr-linux/pokete/server/pokete/user"
    "github.com/lxgr-linux/pokete/server/pokete/users"
)

const HandshakeType msg.Type = "pokete.handshake"

type Handshake struct {
    msg.BaseMsg
    UserName string `json:"user_name"`
    Version  string `json:"version"`
}

func (h Handshake) GetType() msg.Type {
    return HandshakeType
}

func (h Handshake) CallForResponse(ctx context.Context) (msg.Body, error) {
    log.Println("handshake shaken")

    cfg, _ := pctx.ConfigFromContext(ctx)
    client, _ := pctx.ClientFromContext(ctx)
    u, _ := pctx.UsersFromContext(ctx)
    conId, _ := pctx.ConnectionIdFromContext(ctx)

    position := getStartPosition(cfg)

    newUser := user.User{
        Name:     h.UserName,
        Client:   client,
        Position: position,
    }

    if h.Version != cfg.ClientVersion {
        return error2.NewVersionMismatch(cfg.ClientVersion), fmt.Errorf("connection closed")
    }

    err := u.Add(conId, newUser)
    if err == users.USER_PRESENT {
        return error2.NewUserExists(), fmt.Errorf("connection closed")
    }
    if err != nil {
        return nil, err
    }

    return msg.NewEmptyMsg(), nil
}

func getStartPosition(cfg *config.Config) user.Position {
    return user.Position{
        Map: cfg.EntryMap,
        X:   2,
        Y:   9,
    }
}

/*func (h Handshake) Handle(ctx context.Context, c msg.SendClient) error {
    position := getStartPosition(p.Config)
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
      }

    log.Println("handshake shaken")

    return nil
}*/
