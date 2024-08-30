package producer

import (
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/util"
	"google.golang.org/protobuf/compiler/protogen"
	"google.golang.org/protobuf/types/descriptorpb"
)

type ResourceType struct {
	Name   string
	Fields []Field
}

type Field struct {
	Name       string
	PythonType MappedType
	Optional   bool
}

type Model struct {
	Types   []ResourceType
	Package string
}

func NewField(p *Producer, d *descriptorpb.FieldDescriptorProto) Field {
	f := Field{
		Name:       util.ToSnakeCase(*d.Name),
		PythonType: p.MapType(d),
		Optional:   d.Proto3Optional != nil,
	}

	return f
}

func NewResourceType(path string, p *Producer, d *descriptorpb.DescriptorProto) (types []ResourceType) {
	r := ResourceType{Name: *d.Name}

	typeInfo := TypeInfo{Name: *d.Name, IsDict: d.Options != nil && *d.Options.MapEntry}
	p.Types[path+"."+r.Name] = &typeInfo

	for _, nested := range d.NestedType {
		types = append(types, NewResourceType(path+"."+r.Name, p, nested)...)
	}

	if typeInfo.IsDict {
		for _, field := range d.Field {
			typeInfo.DictTypes = append(typeInfo.DictTypes, p.MapType(field))
		}
		return
	}

	for _, field := range d.Field {
		r.Fields = append(r.Fields, NewField(p, field))
	}

	types = append(types, r)

	return
}

func NewModel(file *protogen.File) *Model {
	m := Model{Package: *file.Proto.Package}

	return &m
}
