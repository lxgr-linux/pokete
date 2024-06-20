package resources

type PokeType string

const (
	PokeTypeStone   PokeType = "stone"
	PokeTypeNormal  PokeType = "normal"
	PokeTypePlant   PokeType = "plant"
	PokeTypeFire    PokeType = "fire"
	PokeTypeUndead  PokeType = "undead"
	PokeTypeWater   PokeType = "water"
	PokeTypeBird    PokeType = "bird"
	PokeTypeFlying  PokeType = "flying"
	PokeTypePoison  PokeType = "poison"
	PokeTypeSnake   PokeType = "snake"
	PokeTypeGround  PokeType = "ground"
	PokeTypeElectro PokeType = "electro"
	PokeTypeIce     PokeType = "ice"
)

type Poke struct {
	Name       string     `json:"name"`
	Hp         uint       `json:"hp"`
	Atc        uint       `json:"atc"`
	Defense    uint       `json:"defense"`
	Attacks    []string   `json:"attacks"`
	Pool       []string   `json:"pool"`
	MissChance float32    `json:"miss_chance"`
	LoseXp     uint       `json:"lose_xp"`
	Type       []PokeType `json:"type"`
}

type Pokes map[string]Poke
