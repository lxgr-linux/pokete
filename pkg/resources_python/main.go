package main

import (
	"bytes"
	"log/slog"

	//"fmt"
	"github.com/lxgr-linux/pokete/protoc-gen-pokete-resources-python/producer"
	//"log/slog"
	"text/template"

	//"bytes"
	_ "embed"
	"flag"
	"log"
	"os"

	//"strings"
	//"text/template"

	"google.golang.org/protobuf/compiler/protogen"
)

//go:embed templates/Type.pb.py.tmpl
var fileTmpl string

//go:embed templates/Field.pb.py.tmpl
var fieldTmpl string

//go:embed templates/Unmarshall.pb.py.tmpl
var unmarshallTmpl string

var suffixFlag string

func main() {
	log.SetOutput(os.Stderr)
	flag.StringVar(&suffixFlag, "suffix", ".pb.py", "file suffixFlag")

	protogen.Options{ParamFunc: flag.Set}.Run(func(gen *protogen.Plugin) error {
		gen.SupportedFeatures = 1 // Enables support for optioal fields
		for _, f := range gen.Files {
			if !f.Generate {
				continue
			}
			if err := generateFile(gen, f); err != nil {
				return err
			}
		}
		return nil
	})
}

func generateFile(gen *protogen.Plugin, file *protogen.File) error {
	p := producer.PythonProducer()
	m := p.Produce(file)
	if m == nil {
		return nil
	}

	//slog.Warn(fmt.Sprintf("%+v", m))

	filename := file.GeneratedFilenamePrefix + suffixFlag
	g := gen.NewGeneratedFile(filename, file.GoImportPath)

	tmpl, err := template.New("file").Parse(fileTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.New("field").Parse(fieldTmpl)
	if err != nil {
		return err
	}

	_, err = tmpl.Funcs(template.FuncMap{
		"fieldWithVar": func(field producer.Field, v string) producer.FieldWithVar {
			return producer.FieldWithVar{Field: field, Var: v}
		},
		"pythonTypeWithVar": func(pythonType producer.MappedType, v string) producer.PythonTypeWithVar {
			return producer.PythonTypeWithVar{MappedType: pythonType, Var: v}
		},
		"get": func(field producer.FieldWithVar) string {
			t, _ := template.New("").Parse(`
				{{- if .PythonType.Optional -}}
        			{{ .Var }}.get("{{ .Name }}", None)
				{{- else -}}
        			{{ .Var }}["{{ .Name }}"]
    			{{- end -}}`)
			var buf bytes.Buffer
			err = t.Execute(&buf, field)
			if err != nil {
				slog.Warn(err.Error())
			}
			return buf.String()
		},
	}).New("unmarshall").Parse(unmarshallTmpl)
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
