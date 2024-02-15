CREATE TYPE "division" AS ENUM (
  'Atlantic',
  'Southeast',
  'Central',
  'Northwest',
  'Pacific',
  'Southwest'
);

CREATE TYPE "conference" AS ENUM (
  'East',
  'West'
);

CREATE TYPE "matchs_status" AS ENUM (
  '1',
  '2',
  '3'
);

CREATE TABLE "teams" (
  "id" uuid PRIMARY KEY,
  "name" varchar(50),
  "abrev" varchar(5),
  "logo" text,
  "id_API" real,
  "conference" conference,
  "division" division
);

CREATE TABLE "stats" (
  "id" uuid PRIMARY KEY,
  "match_id" uuid,
  "team_id" uuid,
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
  "id" uuid PRIMARY KEY,
  "id_API" int,
  "date" date,
  "home_team" uuid,
  "away_team" uuid,
  "status" matchs_status,
  "tot_home" int,
  "tot_away" int
);

CREATE TABLE "prediction" (
  "id" uuid PRIMARY KEY,
  "time" timestamp,
  "match_id" uuid,
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
