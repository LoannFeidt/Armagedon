
CREATE TABLE "teams" (
  "id" int PRIMARY KEY,
  "name" varchar(50),
  "abrev" varchar(5),
  "logo" text,
  "conference" varchar(50),
  "division" varchar(50)
);

CREATE TABLE "stats" (
  "game_id" int,
  "team_id" int,
  "fastBreakPoints" int,
  "pointsInPaint" int,
  "biggestLead" int,
  "secondChancePoints" int,
  "pointsOffTurnovers" int,
  "longestRun" int,
  "points" int,
  "fgm" int,
  "fga" int,
  "fgp" real,
  "ftm" int,
  "fta" int,
  "ftp" real,
  "tpm" int,
  "tpa" int,
  "tpp" real,
  "offReb" int,
  "defReb" int,
  "totReb" int,
  "assists" int,
  "pFouls" int,
  "steals" int,
  "turnovers" int,
  "blocks" int,
  "plusMinus" real
);

CREATE TABLE "games" (
  "id" int PRIMARY KEY,
  "date" date,
  "home_team" int,
  "away_team" int,
  "status" int,
  "season" int
);

CREATE TABLE "prediction" (
  "id" int PRIMARY KEY,
  "time" timestamp,
  "game_id" int,
  "prob_win_home" float
);

CREATE INDEX ON "teams" ("abrev");

ALTER TABLE "stats" ADD FOREIGN KEY ("game_id") REFERENCES "games" ("id");

ALTER TABLE "stats" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");

ALTER TABLE "games" ADD FOREIGN KEY ("home_team") REFERENCES "teams" ("id");
ALTER TABLE "games" ADD FOREIGN KEY ("away_team") REFERENCES "teams" ("id");

ALTER TABLE "prediction" ADD FOREIGN KEY ("game_id") REFERENCES "games" ("id");
