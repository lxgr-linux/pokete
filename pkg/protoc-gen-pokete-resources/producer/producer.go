package producer

import (
	"slices"
	"strings"

	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources/identifier"
	"google.golang.org/protobuf/compiler/protogen"
	"google.golang.org/protobuf/types/descriptorpb"
)

type TypeMapper func(d *descriptorpb.FieldDescriptorProto, mt *MappedType)

type TypeInfo struct {
	Name      string
	IsDict    bool
	DictTypes []MappedType
}

type Import struct {
	ImportFile
	Identifier identifier.Identifier
}

type Producer struct {
	Package    *identifier.Identifier
	Model      *Model
	Types      map[string]*TypeInfo
	typeMapper TypeMapper
	Imports    []*Import
}

func (p *Producer) Produce(file *protogen.File) *Model {
	id := identifier.FromIdentifier(string(file.Desc.Package()))
	p.Package = &id
	m := NewModel(file)
	filePath := identifier.FromFile(file)
	if len(file.Proto.MessageType) == 0 {
		return nil
	}

	var identifiers []string

	for i := 0; i < file.Desc.Imports().Len(); i++ {
		imp := file.Desc.Imports().Get(i)

		pathIdentifier := identifier.FromPath(imp.Path()).Relative(filePath.Module()).Module().Identifier()
		if slices.Contains(identifiers, pathIdentifier) {
			continue
		}

		impOb := Import{
			ImportFile{
				IsSameMod:    file.Desc.Package() == imp.Package(),
				Path:         pathIdentifier,
				GoImportPath: identifier.FromUrl(strings.Trim(file.GoImportPath.String(), "\"")).Reduce(id).Extend(identifier.FromIdentifier(string(imp.Package()))).String(),
			},
			identifier.FromIdentifier(string(imp.Package())),
		}

		identifiers = append(identifiers, pathIdentifier)
		p.Imports = append(p.Imports, &impOb)

		//slog.WarnContext(ctx,fmt.Sprintf("%+v", impOb))
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

func GoProducer() Producer {
	return Producer{
		Model:      nil,
		typeMapper: GoTypeMapper,
		Types:      make(map[string]*TypeInfo)}
}
