package util

import "strings"

func ToSnakeCase(identifier string) (result string) {
	for i, char := range identifier {
		if i != 0 && char >= 'A' && char <= 'Z' {
			result += "_"
		}
		result += string(char)
	}
	return strings.ToLower(result)
}

func ToCamelCase(identifier string) (result string) {
	for _, part := range strings.Split(identifier, "_") {
		result += strings.ToUpper(part[0:1]) + part[1:]
	}
	return
}
