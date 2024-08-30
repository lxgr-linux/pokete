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
