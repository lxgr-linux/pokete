// DO NOT EDIT!
// This code was auto generated by the `protoc-gen-pokete-resources` plugin,
// part of the pokete project, by <lxgr@protonmail.com>

package resources

import (
	"github.com/lxgr-linux/pokete/resources/base"
)

type BaseAssets struct {
	Items        map[string]base.Item        `json:"items"`
	Pokes        map[string]base.Poke        `json:"pokes"`
	Attacks      map[string]base.Attack      `json:"attacks"`
	Natures      map[string]base.Nature      `json:"natures"`
	Weathers     map[string]base.Weather     `json:"weathers"`
	Types        map[string]base.Type        `json:"types"`
	SubTypes     []string                    `json:"sub_types"`
	Achievements map[string]base.Achievement `json:"achievements"`
}

type MapTrainers struct {
	Trainers []Trainer `json:"trainers"`
}

type Assets struct {
	Trainers    map[string]MapTrainers `json:"trainers"`
	Npcs        map[string]NPC         `json:"npcs"`
	Obmaps      map[string]Obmap       `json:"obmaps"`
	Stations    map[string]Station     `json:"stations"`
	Decorations map[string]Decoration  `json:"decorations"`
	Maps        map[string]Map         `json:"maps"`
}
