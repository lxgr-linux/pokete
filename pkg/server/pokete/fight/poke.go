package fight

type Nature struct {
	Nature string `json:"nature"`
	Grade  uint   `json:"grade"`
}

type Poke struct {
	Name    string   `json:"name"`
	Xp      uint     `json:"xp"`
	Hp      uint     `json:"hp"`
	Ap      [4]uint  `json:"ap"`
	Effects []string `json:"effects"`
	Attacks []string `json:"attacks"`
	Shiny   bool     `json:"shiny"`
	Nature  Nature   `json:"nature"`
}
