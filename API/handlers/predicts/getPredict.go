package predictsHandlers

import (
	"api-arm/utils"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func (h *handler) GetPredict(context *gin.Context) {
	home_id, err := strconv.Atoi(context.Query("home"))
	if err != nil {
		utils.APIResponse(context, "Missing Home parameter", http.StatusExpectationFailed, http.MethodGet, nil)
		return
	}
	away_id, err := strconv.Atoi(context.Query("away"))
	if err != nil {
		utils.APIResponse(context, "Missing Away parameter", http.StatusExpectationFailed, http.MethodGet, nil)
		return
	}
	predictResponse, statusCode := h.service.GetPredict(home_id, away_id)

	switch statusCode {
	case http.StatusOK:

		utils.APIResponse(context, "SUCESS", http.StatusOK, http.MethodGet, &predictResponse)
		return

	case http.StatusExpectationFailed:
		utils.APIResponse(context, "Internal Server error occured", http.StatusExpectationFailed, http.MethodGet, nil)
		return

	case http.StatusConflict:
		utils.APIResponse(context, "Games already exists. Please try with another games", http.StatusConflict, http.MethodGet, nil)
		return
	case http.StatusCreated:

		utils.APIResponse(context, "SUCESS", http.StatusCreated, http.MethodGet, &predictResponse)
		return
	}

}
