package path

import (
	"google.golang.org/protobuf/compiler/protogen"
	"strings"
)

type Path struct {
	pathItems []string
}

func (p Path) Name() string {
	return p.pathItems[len(p.pathItems)-1]
}

func (p Path) Module() string {
	return strings.Join(p.pathItems[:len(p.pathItems)-1], "/")
}

func (p Path) String() string {
	return strings.Join(p.pathItems, "/")
}

func New(p string) Path {
	return Path{strings.Split(strings.TrimRight(p, ".proto"), "/")}
}

func FromFile(file *protogen.File) Path {
	return New(file.Desc.Path())
}
