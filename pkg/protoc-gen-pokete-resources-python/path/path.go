package path

import (
	"google.golang.org/protobuf/compiler/protogen"
	"slices"
	"strings"
)

type Path struct {
	items []string
}

func (p Path) Name() string {
	return p.items[len(p.items)-1]
}

func (p Path) Module() Path {
	return Path{p.items[:len(p.items)-1]}
}

func (p Path) String() string {
	return strings.Join(p.items, "/")
}

func (p Path) Identifier() string {
	return strings.Join(p.items, ".")
}

func (p Path) Equals(p1 Path) bool {
	return slices.Equal(p.items, p1.items)
}

func (p Path) Relative(base Path) *Path {
	for u := p; len(u.items) >= 0; u = u.Module() {
		if u.Module().Equals(base) {
			return &u
		}
	}
	return nil
}

func New(p string) Path {
	return Path{strings.Split(strings.TrimRight(p, ".proto"), "/")}
}

func FromFile(file *protogen.File) Path {
	return New(file.Desc.Path())
}

func FromIdentifier(id string) Path {
	return Path{strings.Split(id, ".")}
}
