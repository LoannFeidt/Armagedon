package configs

import (
	"log"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type DBConnection interface {
	Connection() *gorm.DB
}

type service struct{}

func NewDBService() *service {
	return &service{}
}

func (s *service) Connection() *gorm.DB {
	databaseURI := "host=127.0.0.1 user=postgres password=postgres dbname=armagedon port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(databaseURI), &gorm.Config{})

	if err != nil {
		defer log.Print("Connection to Database Failed")
		log.Fatal(err.Error())
	} else {
		log.Print("Connection to Database Successfully")
	}

	return db
}

// Proxy function that can be replaced for testing
var Connection = func() *gorm.DB {
	svc := &service{}
	return svc.Connection()
}
