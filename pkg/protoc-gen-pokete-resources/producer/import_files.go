package producer

type ImportFile struct {
	Types        []string
	Path         string
	IsSameMod    bool
	GoImportPath string
}

type ImportFiles []ImportFile
