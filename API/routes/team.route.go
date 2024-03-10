package routes

import (
	teamControllers "api-arm/controllers/team"
	teamHandlers "api-arm/handlers/team"
	teamService "api-arm/services/team"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func InitTeamRoutes(db *gorm.DB, route *gin.RouterGroup) {

	teamRepository := teamControllers.NewTeamRepository(db)
	teamService := teamService.NewTeamService(teamRepository)
	teamHanlders := teamHandlers.NewCreateHandler(teamService)

	route.GET("/", teamHanlders.GetAllTeamsHandler)
}
