package producer

import (
	"fmt"
	"google.golang.org/protobuf/types/descriptorpb"
	"log/slog"
	"strings"
)

type MappedType struct {
	Expression       string
	IsPurelyDomestic bool
	IsRepeated       bool
	IsDict           bool
}

func PythonTypeMapper(p *Producer, d *descriptorpb.FieldDescriptorProto) MappedType {
	var types []string
	var isDict bool
	var isPurelyDomestic bool = true

	switch *d.Type {
	case descriptorpb.FieldDescriptorProto_TYPE_DOUBLE, descriptorpb.FieldDescriptorProto_TYPE_FLOAT:
		types = append(types, "float")
	case descriptorpb.FieldDescriptorProto_TYPE_STRING:
		types = append(types, "str")
	case descriptorpb.FieldDescriptorProto_TYPE_BOOL:
		types = append(types, "bool")
	case descriptorpb.FieldDescriptorProto_TYPE_INT32, descriptorpb.FieldDescriptorProto_TYPE_INT64:
		types = append(types, "int")
	case descriptorpb.FieldDescriptorProto_TYPE_MESSAGE:
		registeredType, ok := p.Types[*d.TypeName]
		if ok {
			if registeredType.IsDict {
				isDict = true
				isPurelyDomestic = isPurelyDomestic && registeredType.DictTypes[0].IsPurelyDomestic && registeredType.DictTypes[1].IsPurelyDomestic
				types = append(
					types,
					fmt.Sprintf(
						"dict[%s, %s]",
						registeredType.DictTypes[0].Expression, registeredType.DictTypes[1].Expression,
					),
				)
			} else {
				isPurelyDomestic = false
				types = append(types, registeredType.Name)
			}
		} else {
			isPurelyDomestic = false
			slog.Warn(fmt.Sprintf("Unregistered type lookup: %s", *d.TypeName))
			types = append(types, *d.TypeName)
		}
	}

	joinedTypes := strings.Join(types, " | ")

	if *d.Label == descriptorpb.FieldDescriptorProto_LABEL_REPEATED && !isDict {
		joinedTypes = fmt.Sprintf("list[%s]", joinedTypes)
	}

	return MappedType{
		Expression:       joinedTypes,
		IsPurelyDomestic: isPurelyDomestic,
		IsDict:           isDict,
	}
}
