package resources

import (
	"encoding/json"
	"os"
	"path"
)

type Resources struct {
	obmaps         *Obmaps
	maps           *Maps
	npcs           *NPCs
	trainers       *Trainers
	mapStations    *MapStations
	mapDecorations *MapDecorations
	pokes          *Pokes
}

func (m Resources) GetObmaps() Obmaps {
	return *m.obmaps
}

func (m Resources) GetMaps() Maps {
	return *m.maps
}

func (m Resources) GetNPCs() NPCs {
	return *m.npcs
}

func (m Resources) GetTrainers() Trainers {
	return *m.trainers
}

func (m Resources) GetMapStations() MapStations {
	return *m.mapStations
}

func (m Resources) GetMapDecorations() MapDecorations {
	return *m.mapDecorations
}

func (m Resources) GetPokes() Pokes {
	return *m.pokes
}

func FromDir(baseDir string) (*Resources, error) {
	tempObmaps, err := readFile[Obmaps](path.Join(baseDir, "map_data.json"))
	if err != nil {
		return nil, err
	}
	tempMaps, err := readFile[Maps](path.Join(baseDir, "maps.json"))
	if err != nil {
		return nil, err
	}
	tempNPCs, err := readFile[NPCs](path.Join(baseDir, "npcs.json"))
	if err != nil {
		return nil, err
	}
	tempTrainers, err := readFile[Trainers](path.Join(baseDir, "trainers.json"))
	if err != nil {
		return nil, err
	}
	tempStations, err := readFile[MapStations](path.Join(baseDir, "map_stations.json"))
	if err != nil {
		return nil, err
	}

	tempDecorations, err := readFile[MapDecorations](path.Join(baseDir, "map_decorations.json"))
	if err != nil {
		return nil, err
	}

	tempPokes, err := readFile[Pokes](path.Join(baseDir, "poketes.json"))
	if err != nil {
		return nil, err
	}

	return &Resources{
		obmaps:         &tempObmaps,
		maps:           &tempMaps,
		npcs:           &tempNPCs,
		trainers:       &tempTrainers,
		mapStations:    &tempStations,
		mapDecorations: &tempDecorations,
		pokes:          &tempPokes,
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
