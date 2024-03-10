package models

type TeamModel struct {
	ID         int    `json:"id"`
	Name       string `json:"name"`
	Abre       string `json:"short"`
	Logo       string `json:"logo"`
	Conference string `json:"conf"`
	Division   string `json:"div"`
	Color      string `json:"color"`
}

func (TeamModel) TableName() string {
	return "teams"
}
