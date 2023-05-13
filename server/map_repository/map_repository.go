package map_repository

import (
	"encoding/json"
	"os"
)

type MapRepo struct {
    obmaps   *Obmaps
    maps     *Maps
    npcs     *NPCs
    trainers *Trainers
}

func (m MapRepo)GetObmaps() Obmaps {
    return *m.obmaps
}

func (m MapRepo)GetMaps() Maps {
    return *m.maps
}

func (m MapRepo)GetNPCs() NPCs {
    return *m.npcs
}

func (m MapRepo)GetTrainers() Trainers {
    return *m.trainers
}

func NewMapRepo() (mapRepo MapRepo, err error) {
	tempObmaps, err := readFile[Obmaps]("res/map_data.json")
	if err != nil {
		return
	}
	tempMaps, err := readFile[Maps]("res/maps.json")
	if err != nil {
		return
	}
	tempNPCs, err := readFile[NPCs]("res/npcs.json")
	if err != nil {
		return
	}
	tempTrainers, err := readFile[Trainers]("res/trainers.json")
	if err != nil {
		return
	}

    return MapRepo {
        obmaps: &tempObmaps,
        maps: &tempMaps,
        npcs: &tempNPCs,
        trainers: &tempTrainers,
    }, nil
}

func readFile[T any](fileName string) (temp T, err error) {
    content, err := os.ReadFile(fileName)
    if err != nil {
        return
    }

    err = json.Unmarshal(content, &temp)

    return
}
