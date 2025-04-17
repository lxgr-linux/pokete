package identifier

import (
	"google.golang.org/protobuf/compiler/protogen"
	"slices"
	"strings"
)

type Identifier struct {
	items []string
}

func (p Identifier) Name() string {
	return p.items[len(p.items)-1]
}

func (p Identifier) Module() Identifier {
	return Identifier{p.items[:len(p.items)-1]}
}

func (p Identifier) String() string {
	return strings.Join(p.items, "/")
}

func (p Identifier) Identifier() string {
	return strings.Join(p.items, ".")
}

func (p Identifier) Equals(p1 Identifier) bool {
	return slices.Equal(p.items, p1.items)
}

func (p Identifier) Len() int {
	return len(p.items)
}

func (p Identifier) Relative(base Identifier) *Identifier {
	for i := len(p.items); i >= 0; i-- {
		if slices.Equal(p.items[:i], base.items) {
			return &Identifier{p.items[i:]}
		}
	}
	return nil
}

func (p Identifier) Extend(i Identifier) Identifier {
	return Identifier{
		items: append(p.items, i.items...),
	}
}

func (p Identifier) Reduce(sub Identifier) Identifier {
	for i := len(p.items); i >= 0; i-- {
		if slices.Equal(p.items[i:], sub.items) {
			return Identifier{p.items[:i]}
		}
	}
	return p
}

func FromPath(p string) Identifier {
	splid := strings.Split(p, ".")
	return Identifier{strings.Split(strings.Join(splid[:len(splid)-1], "/"), "/")}
}

func FromUrl(p string) Identifier {
	return Identifier{strings.Split(p, "/")}
}

func FromFile(file *protogen.File) Identifier {
	return FromPath(file.Desc.Path())
}

func FromIdentifier(id string) Identifier {
	return Identifier{strings.Split(id, ".")}
}
