package msg

import "fmt"

type Registry struct {
	unMarshallers *map[Type]UnMarshaller
}

func (r Registry) GetUnMarshaller(t Type) (UnMarshaller, error) {
	m, ok := (*r.unMarshallers)[t]

	if !ok {
		return nil, fmt.Errorf("can't find type register for type `%s`", t)
	}
	return m, nil
}

func (r Registry) RegisterType(t Type, m UnMarshaller) error {
	_, err := r.GetUnMarshaller(t)
	if err == nil {
		return fmt.Errorf("type `%s` is already registered", t)
	}

	(*r.unMarshallers)[t] = m

	return nil
}

func NewRegistry() Registry {
	m := make(map[Type]UnMarshaller)
	return Registry{&m}
}
