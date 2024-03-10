package gamesService

import (
	gamesControllers "api-arm/controllers/games"
	"api-arm/models"
)

type Service interface {
	GetTodayGames() ([]models.GameModel, int)
}

type service struct {
	repository gamesControllers.Repository
}

func NewGamesService(r gamesControllers.Repository) *service {
	return &service{repository: r}
}

func (s *service) GetTodayGames() ([]models.GameModel, int) {

	return s.repository.GetTodayGames()
}
