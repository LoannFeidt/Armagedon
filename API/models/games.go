package models

import time "time"

type GameModel struct {
	ID        int       `json:"id"`
	Date      time.Time `json:"date"`
	Home_team int       `json:"-"`
	Home      TeamModel `gorm:"foreignKey:Home_team"  json:"home"`
	Away_team int       `json:"-"`
	Away      TeamModel `gorm:"foreignKey:Away_team"  json:"away"`
	Status    int       `json:"status"`
}

func (GameModel) TableName() string {
	return "games"
}
