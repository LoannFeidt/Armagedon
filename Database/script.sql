
CREATE TABLE "teams" (
  "id" int PRIMARY KEY,
  "name" varchar(50),
  "abrev" varchar(5),
  "logo" text,
  "id_API" real,
  "conference" varchar(50),
  "division" varchar(50)
);

CREATE TABLE "stats" (
  "id" int PRIMARY KEY,
  "match_id" int,
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

CREATE TABLE "matchs" (
  "id" int PRIMARY KEY,
  "id_API" int,
  "date" date,
  "home_team" int,
  "away_team" int,
  "status" int
);

CREATE TABLE "prediction" (
  "id" int PRIMARY KEY,
  "time" timestamp,
  "match_id" int,
  "prob_win_home" float
);

CREATE INDEX ON "teams" ("id_API");

CREATE INDEX ON "teams" ("abrev");

CREATE INDEX ON "matchs" ("id_API");

ALTER TABLE "stats" ADD FOREIGN KEY ("match_id") REFERENCES "matchs" ("id");

ALTER TABLE "stats" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");

ALTER TABLE "matchs" ADD FOREIGN KEY ("home_team") REFERENCES "teams" ("id");
ALTER TABLE "matchs" ADD FOREIGN KEY ("away_team") REFERENCES "teams" ("id");

ALTER TABLE "prediction" ADD FOREIGN KEY ("match_id") REFERENCES "matchs" ("id");
