package main

import (
	"bytes"
	_ "embed"
	"flag"
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/module_resolver"
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/path"
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/producer"
	"google.golang.org/protobuf/compiler/protogen"
	"log/slog"
	"maps"
	"text/template"
)

//go:embed templates/File.py.tmpl
var fileTmpl string

//go:embed templates/field.tmpl
var fieldTmpl string

//go:embed templates/unmarshall.tmpl
var unmarshallTmpl string

//go:embed templates/marshall.tmpl
var marshallTmpl string

//go:embed templates/__init__.py.tmpl
var initTmpl string

//go:embed templates/header.tmpl
var headerTmpl string

//go:embed templates/imports.tmpl
var importsTmpl string

var suffixFlag string

func main() {
	flag.StringVar(&suffixFlag, "suffix", ".py", "file suffixFlag")

	protogen.Options{ParamFunc: flag.Set}.Run(func(gen *protogen.Plugin) error {
		gen.SupportedFeatures = 1 // Enables support for optioal fields

		moduleResolver := module_resolver.New()

		for _, f := range gen.Files {
			if !f.Generate {
				continue
			}

			err := generateFile(&moduleResolver, gen, f)
			if err != nil {
				slog.Error(err.Error())
				return err
			}
		}

		err := generateInnitPy(&moduleResolver, gen)
		if err != nil {
			slog.Error(err.Error())
			return err
		}

		return nil
	})
}

func generateInnitPy(moduleResolver *module_resolver.ModuleResolver, gen *protogen.Plugin) error {
	keys := maps.Keys(gen.FilesByPath)

	var filePath *path.Path = nil
	var stringKeys []string

	for s := range keys {
		stringKeys = append(stringKeys, s)
	}

	for _, s := range stringKeys {
		mod := path.New(s).Module()

		if filePath == nil || mod.Len() < filePath.Len() {
			filePath = &mod
		}
	}

	g := gen.NewGeneratedFile(filePath.String()+"/__init__.py", "")

	tmpl, err := template.New("__init__").Parse(initTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("header").Parse(headerTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("imports").Parse(importsTmpl)
	if err != nil {
		return err
	}

	var buf bytes.Buffer
	err = tmpl.Execute(&buf, moduleResolver)
	if err != nil {
		return err
	}

	g.P(buf.String())

	return nil
}

func generateFile(moduleResolver *module_resolver.ModuleResolver, gen *protogen.Plugin, file *protogen.File) error {
	filePath := path.FromFile(file)
	p := producer.PythonProducer()
	m := p.Produce(file)
	if m == nil {
		return nil
	}

	moduleResolver.Add(filePath.Name(), m)

	filename := filePath.String() + suffixFlag
	g := gen.NewGeneratedFile(filename, file.GoImportPath)

	funcs := template.FuncMap{
		"fieldWithVar": func(field producer.Field, v string) producer.FieldWithVar {
			return producer.FieldWithVar{Field: field, Var: v}
		},
		"pythonTypeWithVar": func(pythonType producer.MappedType, v string) producer.PythonTypeWithVar {
			return producer.PythonTypeWithVar{MappedType: pythonType, Var: v}
		},
		"pythonTypeAsBaseType": func(pythonType producer.PythonTypeWithVar) producer.MappedType {
			pythonType.MappedType.IsRepeated = false
			return pythonType.MappedType
		},
		"get": func(field producer.FieldWithVar) string {
			t, err := template.New("abc").Parse(`
				{{- if .PythonType.Optional -}}
        			{{ .Var }}.get("{{ .Name }}", None)
				{{- else -}}
        			{{ .Var }}["{{ .Name }}"]
    			{{- end -}}`)
			if err != nil {
				panic(err.Error())
			}
			var buf bytes.Buffer
			err = t.Execute(&buf, field)
			if err != nil {
				panic(err.Error())
			}
			return buf.String()
		},
	}

	tmpl, err := template.New("file").Funcs(funcs).Parse(fileTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("field").Parse(fieldTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("unmarshall").Parse(unmarshallTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("marshall").Parse(marshallTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("header").Parse(headerTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("imports").Parse(importsTmpl)
	if err != nil {
		return err
	}

	var buf bytes.Buffer
	err = tmpl.Execute(&buf, m)
	if err != nil {
		return err
	}

	g.P(buf.String())

	return nil
}
