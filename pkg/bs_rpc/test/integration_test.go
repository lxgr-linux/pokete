package test

import (
	"slices"
	"testing"

	"github.com/lxgr-linux/pokete/bs_rpc/msg"
	msg1 "github.com/lxgr-linux/pokete/bs_rpc/test/msg"
)

func TestIntegration(t *testing.T) {
	var wanted = []msg.Body{
		msg1.TestResponseMsg{"abcdef"},
		msg1.TestResponseMsg{"4jaja"},
		msg1.TestResponseMsg{"5jaja"},
		msg1.TestResponseMsg{"6jaja"},
		msg1.TestResponseMsg{"7jaja"},
		msg1.TestResponseMsg{"8jaja"},
		msg1.TestResponseMsg{"9jaja"},
		msg1.TestResponseMsg{"10jaja"},
		msg1.TestResponseMsg{"11jaja"},
		msg1.TestResponseMsg{"12jaja"},
		msg1.TestResponseMsg{"13jaja"},
	}
	go testServer()
	var reults = testClient()
	if !slices.Equal(reults, wanted) {
		t.Errorf("got %q, wanted %q", reults, wanted)
	}
}
