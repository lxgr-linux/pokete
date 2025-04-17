package poke

type Nature struct {
	Nature string `json:"nature"`
	Grade  uint   `json:"grade"`
}

type Stats struct {
	OwnershipDate *string `json:"ownership_date"`
	EvolvedDate   *string `json:"evolved_date"`
	TotalBattles  uint32  `json:"total_battles"`
	LostBattles   uint32  `json:"lost_battles"`
	WinBattles    uint32  `json:"win_battles"`
	EarnedXp      uint32  `json:"earned_xp"`
	CaughtWith    string  `json:"caught_with"`
	RunAway       uint32  `json:"run_away"`
}

type Instance struct {
	Name    string   `json:"name"`
	Xp      uint32   `json:"xp"`
	Hp      uint32   `json:"hp"`
	Ap      [4]uint  `json:"ap"`
	Effects []string `json:"effects"`
	Attacks []string `json:"attacks"`
	Shiny   bool     `json:"shiny"`
	Nature  Nature   `json:"nature"`
	Stats   Stats    `json:"stats"`
}
