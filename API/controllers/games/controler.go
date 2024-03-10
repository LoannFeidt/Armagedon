package gamesControllers

import (
	"api-arm/models"
	"net/http"
	"time"

	"gorm.io/gorm"
)

type Repository interface {
	GetTodayGames() ([]models.GameModel, int)
}

type repository struct {
	db *gorm.DB
}

func NewGamesRepository(db *gorm.DB) *repository {
	return &repository{db: db}
}

func (repo *repository) GetTodayGames() ([]models.GameModel, int) {
	var games []models.GameModel
	db := repo.db
	today := time.Now()
	checkIfGamesExists := db.Limit(10).Find(&games)

	db.Where(
		&models.GameModel{Status: 1, Date: today}).
		Preload("Away").
		Preload("Home").
		Find(&games)
	if checkIfGamesExists.Error != nil {
		return nil, http.StatusNotFound
	}
	return games, http.StatusOK
}
