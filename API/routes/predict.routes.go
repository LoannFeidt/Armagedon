package routes

import (
	predictsControllers "api-arm/controllers/predicts"
	predictsHandlers "api-arm/handlers/predicts"
	predictsService "api-arm/services/predict"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func InitGamesPrediction(db *gorm.DB, route *gin.RouterGroup) {

	predictsRepository := predictsControllers.NewPredictsRepository(db)
	predictsService := predictsService.NewPredictsService(predictsRepository)
	predictsHanlders := predictsHandlers.NewCreateHandler(predictsService)

	route.GET("/", predictsHanlders.GetPredict)
}
