package util

import "slices"

var allKeywords = []string{"False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"}

func KeywordSafe(name string) string {
	if slices.Contains(allKeywords, name) {
		return name + "_"
	}
	return name
}
