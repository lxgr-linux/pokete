package map_repository

import (
	"encoding/json"
	"os"
	"sync"
)

const (
	MAP = "playmap_18"
)

var (
	obmaps *Obmaps
	maps   *Maps
	once   sync.Once
)

func Read() error {
	mapDataContent, err := os.ReadFile("res/map_data.json")
	if err != nil {
		return err
	}
	mapContent, err := os.ReadFile("res/maps.json")
	if err != nil {
		return err
	}

	tempObmaps := Obmaps{}
	tempMaps := Maps{}
	err = json.Unmarshal(mapDataContent, &tempObmaps)
	if err != nil {
		return err
	}
	err = json.Unmarshal(mapContent, &tempMaps)
	if err != nil {
		return err
	}

	once.Do(func() {
		obmaps = &tempObmaps
		maps = &tempMaps
	})

	return nil
}

func GetObmap() Obmap {
	return (*obmaps)[MAP]
}

func GetMap() Map {
	return (*maps)[MAP]
}
