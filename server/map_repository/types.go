package map_repository

type Obmaps map[string]Obmap

type Obmap struct {
	HardObs map[string]Ob   `json:"hard_obs"`
	SoftObs map[string]Ob   `json:"soft_obs"`
	Dors    map[string]Dor  `json:"dors"`
	Balls   map[string]Ball `json:"balls"`
}

type Ob struct {
	X   int32  `json:"x"`
	Y   int32  `json:"y"`
	Txt string `json:"txt"`
}

type Dor struct {
	X    int32   `json:"x"`
	Y    int32   `json:"y"`
	Args DorArgs `json:"args"`
}

type DorArgs struct {
	Map string `json:"map"`
	X   int32  `json:"x"`
	Y   int32  `json:"y"`
}

type Ball struct {
	X int32 `json:"x"`
	Y int32 `json:"y"`
}

type Maps map[string]Map

type Map struct {
	Height       int32     `json:"height"`
	Width        int32     `json:"width"`
	Song         string    `json:"song"`
	PrettyName   string    `json:"pretty_name"`
	ExtraActions *string   `json:"extra_actions"`
	PokeArgs     *PokeArgs `json:"poke_args"`
	WPokeArgs    *PokeArgs `json:"w_poke_args"`
	Weather      *string   `json:"weather"`
}

type PokeArgs struct {
	Pokes  []string `json:"pokes"`
	Minlvl int32    `json:"minlvl"`
	Maxlvl int32    `json:"maxlvl"`
}

type NPCs map[string]NPC

type NPC struct {
	Texts []string `json:"texts"`
	Fn   *string  `json:"fn"`
	Map  string   `json:"map"`
	X    int32    `json:"x"`
	Y    int32    `json:"y"`
	Chat *Chat    `json:"chat"`
}

type Chat struct {
	Q []string        `json:"q"`
	A map[string]Chat `json:"a"`
}

type Trainers map[string][]Trainer

type Trainer struct {
	Pokes []TrainerPokeArgs `json:"pokes"`
	Args  TrainerArgs       `json:"args"`
}

type TrainerPokeArgs struct {
	Name string `json:"name"`
	Xp   int32  `json:"xp"`
}

type TrainerArgs struct {
	Name      string   `json:"name"`
	Gender    string   `json:"gender"`
	Texts     []string `json:"texts"`
	LoseTexts []string `json:"lose_texts"`
	WinTexts  []string `json:"win_texts"`
	X         int32    `json:"x"`
	Y         int32    `json:"y"`
}
