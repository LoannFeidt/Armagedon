package routes

import (
	gamesControllers "api-arm/controllers/games"
	gamesHandlers "api-arm/handlers/games"
	gamesService "api-arm/services/games"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func InitGamesRoutes(db *gorm.DB, route *gin.RouterGroup) {

	gamesRepository := gamesControllers.NewGamesRepository(db)
	gamesService := gamesService.NewGamesService(gamesRepository)
	gamesHanlders := gamesHandlers.NewCreateHandler(gamesService)

	route.GET("/today", gamesHanlders.GetTodayGamesHandler)
}
