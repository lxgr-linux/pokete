package fight

import "errors"

var FIGHT_DOESNT_EXIST = errors.New("fight with id doesnt exist")

type FightID uint64

type Fights struct {
	currFightID FightID
	fights      map[FightID]*Fight
}

func (f *Fights) incID() {
	f.currFightID += 1
}

func (f *Fights) Add(fight *Fight) {
	f.incID()
	fight.ID = f.currFightID
	f.fights[fight.ID] = fight
}

func (f *Fights) Get(id FightID) (*Fight, error) {
	fight, ok := f.fights[id]
	if !ok {
		return nil, FIGHT_DOESNT_EXIST
	}
	return fight, nil
}

func NewFights() Fights {
	return Fights{0, make(map[FightID]*Fight)}
}
