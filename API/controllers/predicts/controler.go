package predictsControllers

import (
	"api-arm/models"
	"fmt"
	"net/http"
	"time"

	"gorm.io/gorm"
)

type Repository interface {
	GetPredict(home_id int, away_id int) (*models.PredictionModel, int)
}

type repository struct {
	db *gorm.DB
}

func NewPredictsRepository(db *gorm.DB) *repository {
	return &repository{db: db}
}

func (repo *repository) GetPredict(home_id int, away_id int) (*models.PredictionModel, int) {

	db := repo.db
	today := time.Now()
	prediction := models.PredictionModel{
		Home_team: home_id,
		Away_team: away_id,
		Date:      today,
	}
	checkIfGamesExists := db.Where(prediction).Preload("Away").
		Preload("Home").
		First(&prediction)

	if checkIfGamesExists.Error != nil {
		pred_score := 0.45
		prediction := models.PredictionModel{
			Home_team:     home_id,
			Away_team:     away_id,
			Date:          today,
			Prob_win_home: pred_score,
		}
		create := db.Create(&prediction)
		db.Where(prediction).Preload("Away").
			Preload("Home").
			First(&prediction)
		if create.Error != nil {
			return nil, http.StatusExpectationFailed
		}

		return &prediction, http.StatusCreated
	}
	fmt.Println("ICI")
	return &prediction, http.StatusOK
}