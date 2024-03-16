package models

import "time"

type PredictionModel struct {
	ID            int       `json:"id"`
	Date          time.Time `json:"date"`
	Home_team     int       `json:"-"`
	Home          TeamModel `gorm:"foreignKey:Home_team"  json:"home"`
	Away_team     int       `json:"-"`
	Away          TeamModel `gorm:"foreignKey:Away_team"  json:"away"`
	Prob_win_home float64   `json:"prob_home"`
}

func (PredictionModel) TableName() string {
	return "prediction"
}
