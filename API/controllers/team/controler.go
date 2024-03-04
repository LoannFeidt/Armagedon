package teamControllers

import (
	"api-arm/models"
	"net/http"

	"gorm.io/gorm"
)

type Repository interface {
	GetAllTeams() ([]models.TeamModel, int)
}

type repository struct {
	db *gorm.DB
}

func NewTeamRepository(db *gorm.DB) *repository {
	return &repository{db: db}
}

func (repo *repository) GetAllTeams() ([]models.TeamModel, int) {
	var teams []models.TeamModel
	db := repo.db

	checkIfTeamsExists := db.Find(&teams)
	if checkIfTeamsExists.Error != nil {
		return nil, http.StatusNotFound
	}
	return teams, http.StatusOK
}
