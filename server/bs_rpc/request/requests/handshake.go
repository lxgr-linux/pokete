package requests

type RequestHandshake struct {
    UserName string
    Version  string
}

func (r RequestHandshake) Handle(connection *net.Conn, p provider.Provider) error {
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

    return nil
}

func getStartPosition(cfg config.Config) user_repository.Position {
    return user_repository.Position{
        Map: cfg.EntryMap,
        X:   2,
        Y:   9,
    }
}
