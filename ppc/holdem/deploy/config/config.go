package config

import (
	"github.com/ilyakaznacheev/cleanenv"
	"log"
	"time"
)

type Config struct {
	Flag    string        `env:"FLAG" env-required:"true"`
	Levels  int           `env:"LEVELS" env-default:"1000"`
	Addr    string        `env:"ADDR" env-default:":8080"`
	Timeout time.Duration `env:"TIMEOUT" env-default:"60s"`

	initialized bool
}

var config Config

func GetConfig() Config {
	if config.initialized {
		return config
	}

	if err := cleanenv.ReadEnv(&config); err != nil {
		log.Fatal(err)
	}
	config.initialized = true

	return config
}
