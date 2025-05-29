from pydantic import BaseModel, Field



# PLAYERS' LEADERBOARD
class BasePlayerBasicStatisticsSchema(BaseModel):
    player_name: str = Field(min_length=1)

class PlayerPointBasicStatisticsSchema(BasePlayerBasicStatisticsSchema):
    total_points: int = Field(ge=0, default=0, multiple_of=5)
    bonus_points: int = Field(ge=0, default=0, multiple_of=5)

class PlayerGBasicStatisticsSchema(BasePlayerBasicStatisticsSchema):
    total_g: int = Field(ge=0, default=0)

class PlayerDBasicStatisticsSchema(BasePlayerBasicStatisticsSchema):
    total_d: int = Field(ge=0, default=0)

class PlayerCorrectnessBasicStatisticsSchema(BasePlayerBasicStatisticsSchema):
    total_correct_answers: int = Field(ge=0, default=0)


class YellowPlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerPointBasicStatisticsSchema]

class WhitePlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerPointBasicStatisticsSchema]

class RedPlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerPointBasicStatisticsSchema]

class PinkPlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerPointBasicStatisticsSchema]

class BluePlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerGBasicStatisticsSchema]

class OrangePlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerDBasicStatisticsSchema]

class GreenPlayerLeaderboardSchema(BaseModel):
    leaderboard: list[PlayerCorrectnessBasicStatisticsSchema]



# TEAMS' LEADERBOARD
class BaseTeamStatisticsSchema(BaseModel):
    team_name: str = Field(min_length=1)
    total_points: int = Field(ge=0, default=0, multiple_of=5)

class TeamBasicStatisticsSchema(BaseTeamStatisticsSchema):
    pass

class TeamLeaderboardSchema(BaseModel):
    leaderboard: list[TeamBasicStatisticsSchema]