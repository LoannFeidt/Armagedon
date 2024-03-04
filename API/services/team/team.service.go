package teamService

import (
	teamControllers "api-arm/controllers/team"
	"api-arm/models"
)

type Service interface {
	GetAllTeams() ([]models.TeamModel, int)
}

type service struct {
	repository teamControllers.Repository
}

func NewTeamService(r teamControllers.Repository) *service {
	return &service{repository: r}
}

func (s *service) GetAllTeams() ([]models.TeamModel, int) {

	return s.repository.GetAllTeams()
}
