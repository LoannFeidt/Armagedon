package teamHandlers

import (
	teamService "api-arm/services/team"
)

type handler struct {
	service teamService.Service
}

func NewCreateHandler(service teamService.Service) *handler {
	return &handler{service: service}
}
