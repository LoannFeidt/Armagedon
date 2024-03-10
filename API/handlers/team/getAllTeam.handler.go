package teamHandlers

import (
	"api-arm/utils"
	"net/http"

	"github.com/gin-gonic/gin"
)

func (h *handler) GetAllTeamsHandler(context *gin.Context) {

	teamResponse, statusCode := h.service.GetAllTeams()

	switch statusCode {
	case http.StatusOK:

		utils.APIResponse(context, "Received teams", http.StatusOK, http.MethodGet, &teamResponse)
		return

	case http.StatusExpectationFailed:
		utils.APIResponse(context, "Internal Server error occured", http.StatusExpectationFailed, http.MethodGet, nil)
		return

	case http.StatusConflict:
		utils.APIResponse(context, "Teams already exists. Please try with another teams", http.StatusConflict, http.MethodGet, nil)
		return
	}
}
