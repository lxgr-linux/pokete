package config

import (
	"os"

	"github.com/joho/godotenv"
	"gopkg.in/yaml.v3"
)

type Config struct {
	ServerHost    string
	ServerPort    string
	APIPort       string
	ServerType    string
	ClientVersion string
	EntryMap      string
}

func getEnvWithFallBack(envName, fallback string) (env string) {
	env = os.Getenv(envName)
	if env == "" {
		env = fallback
	}
	return
}

func FromEnv() Config {
	godotenv.Load(".env")
	return Config{
		ServerHost:    getEnvWithFallBack("POKETE_SERVER_HOST", "localhost"),
		ServerPort:    getEnvWithFallBack("POKETE_SERVER_PORT", "9988"),
		APIPort:       getEnvWithFallBack("POKETE_API_PORT", "9989"),
		ServerType:    getEnvWithFallBack("POKETE_SERVER_TYPE", "tcp"),
		ClientVersion: getEnvWithFallBack("POKETE_SERVER_CLIENT_VERSION", "0.9.2"),
		EntryMap:      getEnvWithFallBack("POKETE_SERVER_CLIENT_ENTRYMAP", "servermap_1"),
	}
}

func FromYAML(path string) (*Config, error) {
	var config Config
	file, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	err = yaml.Unmarshal(file, &config)

	return &config, err
}
