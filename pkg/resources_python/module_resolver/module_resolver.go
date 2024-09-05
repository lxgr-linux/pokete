package module_resolver

import (
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/producer"
)

type File struct {
	Types []string
	Path  string
}

type ModuleResolver []File

func (m *ModuleResolver) Add(name string, model *producer.Model) {
	var types []string
	for _, t := range model.Types {
		types = append(types, t.Name)
	}

	*m = append(*m, File{Types: types, Path: name})
}

func New() ModuleResolver {
	return ModuleResolver{}
}
