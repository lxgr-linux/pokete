package status

import (
	"encoding/json"
    "log"
	"net/http"

    "github.com/lxgr-linux/pokete/server/provider"
)

type status struct {
	UsersOnline []string
}

type statusHandler struct {
	p provider.Provider
}

func NewStatusHandler(p provider.Provider) statusHandler {
    return statusHandler{p}
}

func (s statusHandler) HandleRequests() {
	http.HandleFunc("/status", s.handleStatus)
	log.Print("Serving status API at " + s.p.Config.ServerHost + ":" + s.p.Config.APIPort + "/status")
	log.Fatal(http.ListenAndServe(":"+s.p.Config.APIPort, nil))
}

func (s statusHandler) handleStatus(w http.ResponseWriter, r *http.Request) {
	log.Print("Endpoint Hit: status")
	json.NewEncoder(w).Encode(status{
		UsersOnline: s.p.UserRepo.GetAllUserNames(),
	})
}
