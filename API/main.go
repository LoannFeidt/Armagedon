package main

import (
	"api-arm/configs"
	"api-arm/routes"
	"api-arm/utils"
	"log"

	"github.com/gin-gonic/gin"
)

func main() {
	router := SetupAppRouter()
	log.Fatal(router.Run(":" + utils.GodotEnv("GO_PORT")))
}

func SetupAppRouter() *gin.Engine {

	db := configs.Connection()

	router := gin.Default()

	gin.SetMode(gin.TestMode)

	api := router.Group("api/v1")

	team := api.Group("/team")

	routes.InitTeamRoutes(db, team)

	return router
}
