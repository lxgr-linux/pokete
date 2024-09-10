package producer

import (
	"fmt"
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/path"
	"google.golang.org/protobuf/types/descriptorpb"
	"log/slog"
	"slices"
	"strings"
)

type MappedType struct {
	Expression       string
	IsPurelyDomestic bool
	IsRepeated       bool
	IsDict           bool
	DictField1       *MappedType
	DictField2       *MappedType
	Optional         bool
}

func PythonTypeMapper(p *Producer, d *descriptorpb.FieldDescriptorProto) (mt MappedType) {
	mt.IsPurelyDomestic = true
	mt.Optional = d.Proto3Optional != nil
	mt.IsRepeated = *d.Label == descriptorpb.FieldDescriptorProto_LABEL_REPEATED
	switch *d.Type {
	case descriptorpb.FieldDescriptorProto_TYPE_DOUBLE, descriptorpb.FieldDescriptorProto_TYPE_FLOAT:
		mt.Expression = "float"
	case descriptorpb.FieldDescriptorProto_TYPE_STRING:
		mt.Expression = "str"
	case descriptorpb.FieldDescriptorProto_TYPE_BOOL:
		mt.Expression = "bool"
	case descriptorpb.FieldDescriptorProto_TYPE_INT32, descriptorpb.FieldDescriptorProto_TYPE_INT64:
		mt.Expression = "int"
	case descriptorpb.FieldDescriptorProto_TYPE_MESSAGE:
		registeredType, ok := p.Types[*d.TypeName]
		if ok {
			if registeredType.IsDict {
				mt.IsDict = true
				mt.IsPurelyDomestic = mt.IsPurelyDomestic && registeredType.DictTypes[0].IsPurelyDomestic && registeredType.DictTypes[1].IsPurelyDomestic
				mt.DictField1 = &registeredType.DictTypes[0]
				mt.DictField2 = &registeredType.DictTypes[1]
			} else {
				mt.IsPurelyDomestic = false
				mt.Expression = registeredType.Name
			}
		} else {
			mt.IsPurelyDomestic = false
			typeIdentifier := path.FromIdentifier(strings.TrimLeft(*d.TypeName, "."))

			for _, imp := range p.Imports {
				if imp.Identifier.Equals(typeIdentifier.Module()) {
					mt.Expression = typeIdentifier.Name()
					if !slices.Contains(imp.Types, mt.Expression) {
						imp.Types = append(imp.Types, mt.Expression)
					}
					return
				}
			}

			slog.Warn(fmt.Sprintf("Unregistered type lookup: %s", *d.TypeName))
			mt.Expression = *d.TypeName
		}
	}

	return
}
