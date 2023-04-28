package config

import (
	"os"
	"sync"
    
    "github.com/joho/godotenv"
)

type Config struct {
	ServerHost    string
	ServerPort    string
	ServerType    string
	ClientVersion string
}

var (
	config *Config
	once   sync.Once
)

func getEnvWithFallBack(envName, fallback string) (env string) {
	env = os.Getenv(envName)
	if env == "" {
		env = fallback
	}
	return
}

func Init() {
    godotenv.Load(".env")
	once.Do(func() {
		config = &Config{
			ServerHost:    getEnvWithFallBack("POKETE_SERVER_HOST", "localhost"),
			ServerPort:    getEnvWithFallBack("POKETE_SERVER_PORT", "9988"),
			ServerType:    getEnvWithFallBack("POKETE_SERVER_TYPE", "tcp"),
			ClientVersion: getEnvWithFallBack("POKETE_SERVER_CLIENT_VERSION", "0.9.1"),
		}
	})
}

func Get() Config {
    return *config
}