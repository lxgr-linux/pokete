package handler

import (
    "encoding/json"
    
    "github.com/lxgr-linux/pokete/server/requests"
)

func unmarshallRequest[T requests.RequestBody](res []byte, genericResponseObject *requests.Request[requests.RequestBody]) error {
	responseObject := requests.Request[T]{}
	err := json.Unmarshal(res, &responseObject)
	if err != nil {
		return err
	}

	genericResponseObject.Body = responseObject.Body

	return nil
}

func Handle(res []byte) (genericResponseObject requests.Request[requests.RequestBody],  err error) {
	err = json.Unmarshal(res, &genericResponseObject)

	switch genericResponseObject.Type {
	case requests.RequestType_POSITION_UPDATE:
		err = unmarshallRequest[requests.RequestPosition](res, &genericResponseObject)
		if err != nil {
			return
		}
	case requests.RequestType_HANDSHAKE:
		err = unmarshallRequest[requests.RequestHandshake](res, &genericResponseObject)
		if err != nil {
			return
		}
	}
    return
}
