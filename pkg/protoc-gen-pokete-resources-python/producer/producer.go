package producer

import (
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/path"
	"google.golang.org/protobuf/compiler/protogen"
	"google.golang.org/protobuf/types/descriptorpb"
)

type TypeMapper func(p *Producer, d *descriptorpb.FieldDescriptorProto) MappedType

type TypeInfo struct {
	Name      string
	IsDict    bool
	DictTypes []MappedType
}

type Import struct {
	ImportFile
	Identifier path.Path
}

type Producer struct {
	Model      *Model
	Types      map[string]*TypeInfo
	typeMapper TypeMapper
	Imports    []*Import
}

func (p *Producer) MapType(d *descriptorpb.FieldDescriptorProto) MappedType {
	return p.typeMapper(p, d)
}

func (p *Producer) Produce(file *protogen.File) *Model {
	m := NewModel(file)
	filePath := path.FromFile(file)
	if len(file.Proto.MessageType) == 0 {
		return nil
	}

	for i := 0; i < file.Desc.Imports().Len(); i++ {
		imp := file.Desc.Imports().Get(i)

		p.Imports = append(p.Imports, &Import{
			ImportFile{Path: path.New(imp.Path()).Relative(filePath.Module()).Identifier()},
			path.FromIdentifier(string(imp.Package())),
		})
	}

	for _, message := range file.Proto.MessageType {
		m.Types = append(m.Types, NewResourceType("."+m.Package.Identifier(), p, message)...)
	}

	for _, imp := range p.Imports {
		m.Imports = append(m.Imports, imp.ImportFile)
	}

	return m
}

func PythonProducer() Producer {
	return Producer{
		Model:      nil,
		typeMapper: PythonTypeMapper,
		Types:      make(map[string]*TypeInfo)}
}
