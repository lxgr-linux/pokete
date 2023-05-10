package status

import (
    "encoding/json"
    "github.com/lxgr-linux/pokete/server/config"
    "github.com/lxgr-linux/pokete/server/user_repository"
    "log"
    "net/http"
)

type status struct {
    UsersOnline []string
}

func HandleRequests() {
    http.HandleFunc("/status", handleStatus)
    log.Print("Serving status API at " + config.Get().ServerHost + ":" + config.Get().APIPort + "/status")
    log.Fatal(http.ListenAndServe(":" + config.Get().APIPort, nil))
}

func handleStatus(w http.ResponseWriter, r *http.Request) {
    log.Print("Endpoint Hit: status")
    json.NewEncoder(w).Encode(status{
        UsersOnline: user_repository.GetAllUserNames(),
    })
}