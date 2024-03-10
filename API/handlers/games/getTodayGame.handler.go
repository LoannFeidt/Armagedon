package gamesHandlers

import (
	"api-arm/utils"
	"net/http"

	"github.com/gin-gonic/gin"
)

func (h *handler) GetTodayGamesHandler(context *gin.Context) {

	gamesResponse, statusCode := h.service.GetTodayGames()

	switch statusCode {
	case http.StatusOK:

		utils.APIResponse(context, "Received games", http.StatusOK, http.MethodGet, &gamesResponse)
		return

	case http.StatusExpectationFailed:
		utils.APIResponse(context, "Internal Server error occured", http.StatusExpectationFailed, http.MethodGet, nil)
		return

	case http.StatusConflict:
		utils.APIResponse(context, "Games already exists. Please try with another games", http.StatusConflict, http.MethodGet, nil)
		return
	}
}
