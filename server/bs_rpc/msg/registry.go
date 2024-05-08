package msg

import "fmt"

type Registry struct {
	types *map[Type]Body
}

func (r Registry) GetType(t Type) (Body, error) {
	body, ok := (*r.types)[t]

	if !ok {
		return nil, fmt.Errorf("can't find type register for type `%s`", t)
	}
	return body, nil
}

func (r Registry) RegisterType(b Body) error {
	t := b.GetType()

	_, err := r.GetType(t)
	if err == nil {
		return fmt.Errorf("type `%s` is already registered", t)
	}

	(*r.types)[t] = b

	return nil
}

func NewRegistry() Registry {
	m := make(map[Type]Body)
	return Registry{&m}
}
