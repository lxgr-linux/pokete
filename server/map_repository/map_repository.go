package map_repository

import (
	"encoding/json"
	"os"
	"sync"
)

var (
	obmaps   *Obmaps
	maps     *Maps
	npcs     *NPCs
	trainers *Trainers
	once     sync.Once
)

func readFile[T any](fileName string) (temp T, err error) {
	content, err := os.ReadFile(fileName)
	if err != nil {
		return
	}

	err = json.Unmarshal(content, &temp)

	return
}

func Read() error {
	tempObmaps, err := readFile[Obmaps]("res/map_data.json")
	if err != nil {
		return err
	}
	tempMaps, err := readFile[Maps]("res/maps.json")
	if err != nil {
		return err
	}
	tempNPCs, err := readFile[NPCs]("res/npcs.json")
	if err != nil {
		return err
	}
	tempTrainers, err := readFile[Trainers]("res/trainers.json")
	if err != nil {
		return err
	}

	once.Do(func() {
		obmaps = &tempObmaps
		maps = &tempMaps
		npcs = &tempNPCs
		trainers = &tempTrainers
	})

	return nil
}

func GetObmaps() Obmaps {
	return *obmaps
}

func GetMaps() Maps {
	return *maps
}

func GetNPCs() NPCs {
	return *npcs
}

func GetTrainers() Trainers {
	return *trainers
}
