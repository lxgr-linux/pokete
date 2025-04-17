package producer

import (
	"fmt"
	"log/slog"
	"slices"
	"strings"

	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources/identifier"
	"google.golang.org/protobuf/types/descriptorpb"
)

type MappedType struct {
	Package          string
	Expression       string
	IsPurelyDomestic bool
	IsRepeated       bool
	IsDict           bool
	DictField1       *MappedType
	DictField2       *MappedType
	Optional         bool
}

func (p *Producer) MapType(d *descriptorpb.FieldDescriptorProto) (mt MappedType) {
	mt.IsPurelyDomestic = true
	mt.Optional = d.Proto3Optional != nil
	mt.IsRepeated = *d.Label == descriptorpb.FieldDescriptorProto_LABEL_REPEATED
	switch *d.Type {
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
			typeIdentifier := identifier.FromIdentifier(strings.TrimLeft(*d.TypeName, "."))

			if !typeIdentifier.Module().Equals(*p.Package) {
				mt.Package = typeIdentifier.Module().Name() + "."
			}

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
	default:
		p.typeMapper(d, &mt)
	}

	return
}

func PythonTypeMapper(d *descriptorpb.FieldDescriptorProto, mt *MappedType) {
	switch *d.Type {
	case descriptorpb.FieldDescriptorProto_TYPE_DOUBLE, descriptorpb.FieldDescriptorProto_TYPE_FLOAT:
		mt.Expression = "float"
	case descriptorpb.FieldDescriptorProto_TYPE_STRING:
		mt.Expression = "str"
	case descriptorpb.FieldDescriptorProto_TYPE_BOOL:
		mt.Expression = "bool"
	case descriptorpb.FieldDescriptorProto_TYPE_INT32, descriptorpb.FieldDescriptorProto_TYPE_INT64, descriptorpb.FieldDescriptorProto_TYPE_UINT32, descriptorpb.FieldDescriptorProto_TYPE_UINT64:
		mt.Expression = "int"
	case descriptorpb.FieldDescriptorProto_TYPE_BYTES:
		mt.Expression = "bytes"
	}
}

func GoTypeMapper(d *descriptorpb.FieldDescriptorProto, mt *MappedType) {
	switch *d.Type {
	case descriptorpb.FieldDescriptorProto_TYPE_FLOAT:
		mt.Expression = "float32"
	case descriptorpb.FieldDescriptorProto_TYPE_DOUBLE:
		mt.Expression = "float64"
	case descriptorpb.FieldDescriptorProto_TYPE_STRING:
		mt.Expression = "string"
	case descriptorpb.FieldDescriptorProto_TYPE_BOOL:
		mt.Expression = "bool"
	case descriptorpb.FieldDescriptorProto_TYPE_INT32:
		mt.Expression = "int32"
	case descriptorpb.FieldDescriptorProto_TYPE_INT64:
		mt.Expression = "int64"
	case descriptorpb.FieldDescriptorProto_TYPE_UINT32:
		mt.Expression = "uint32"
	case descriptorpb.FieldDescriptorProto_TYPE_UINT64:
		mt.Expression = "uint64"
	case descriptorpb.FieldDescriptorProto_TYPE_BYTES:
		mt.Expression = "[]byte"
	}
}
