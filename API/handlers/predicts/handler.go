package predictsHandlers

import (
	predictsService "api-arm/services/predict"
)

type handler struct {
	service predictsService.Service
}

func NewCreateHandler(service predictsService.Service) *handler {
	return &handler{service: service}
}
