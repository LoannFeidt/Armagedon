package predictsService

import (
	predictsControllers "api-arm/controllers/predicts"
	"api-arm/models"
)

type Service interface {
	GetPredict(home_id int, away_id int) (*models.PredictionModel, int)
}

type service struct {
	repository predictsControllers.Repository
}

func NewPredictsService(r predictsControllers.Repository) *service {
	return &service{repository: r}
}

func (s *service) GetPredict(home_id int, away_id int) (*models.PredictionModel, int) {

	return s.repository.GetPredict(home_id, away_id)
}
