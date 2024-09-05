package producer

import (
	"google.golang.org/protobuf/compiler/protogen"
	"google.golang.org/protobuf/types/descriptorpb"
)

type TypeMapper func(p *Producer, d *descriptorpb.FieldDescriptorProto) MappedType

type TypeInfo struct {
	Name      string
	IsDict    bool
	DictTypes []MappedType
}

type Producer struct {
	Model      *Model
	Types      map[string]*TypeInfo
	typeMapper TypeMapper
}

func (p *Producer) MapType(d *descriptorpb.FieldDescriptorProto) MappedType {
	return p.typeMapper(p, d)
}

func (p *Producer) Produce(file *protogen.File) *Model {
	m := NewModel(file)
	if len(file.Proto.MessageType) == 0 {
		return nil
	}

	for _, message := range file.Proto.MessageType {
		m.Types = append(m.Types, NewResourceType("."+m.Package, p, message)...)
	}

	return m
}

func PythonProducer() Producer {
	return Producer{
		Model:      nil,
		typeMapper: PythonTypeMapper,
		Types:      make(map[string]*TypeInfo)}
}
