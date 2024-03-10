package gamesHandlers

import (
	gamesService "api-arm/services/games"
)

type handler struct {
	service gamesService.Service
}

func NewCreateHandler(service gamesService.Service) *handler {
	return &handler{service: service}
}
