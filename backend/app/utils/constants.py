from enum import Enum

class GameScores:
    SINGLE_THROW_MIN = -40 # kaikki pappi-kyykät rajalta sisään
    SINGLE_THROW_MAX = 80 #kaikki kyykät ulos
    ROUND_SCORE_MIN = -80 # 40 kyykkää * 2p 
    ROUND_SCORE_MAX = 19 # yhdellä heitolla kaiki kyykät ulos ja 1 piste käyttämättömästä heitosta henkkarikentällä
    TOTAL_SCORE_MIN = ROUND_SCORE_MIN * 2  # -160
    TOTAL_SCORE_MAX = ROUND_SCORE_MAX * 2  # 38

    @classmethod
    def validate_throw(cls, value: int) -> bool:
        return cls.SINGLE_THROW_MIN <= value <= cls.SINGLE_THROW_MAX

    @classmethod
    def validate_round_score(cls, value: int) -> bool:
        return cls.ROUND_SCORE_MIN <= value <= cls.ROUND_SCORE_MAX

    @classmethod
    def validate_total_score(cls, value: int) -> bool:
        return cls.TOTAL_SCORE_MIN <= value <= cls.TOTAL_SCORE_MAX

class FormDefaults:
    NO_PLAYER_CHOICE = ('-1', '-- Select Player --')
    NO_PLAYERS_LIST = [('-1', 'No players')]

class FormFields:
    PLAYER_1 = 'player_1'
    PLAYER_2 = 'player_2'
    THROW_1 = 'throw_1'
    THROW_2 = 'throw_2'
    THROW_3 = 'throw_3'
    THROW_4 = 'throw_4'
    
    SCORE_1_1 = 'score_1_1'
    SCORE_1_2 = 'score_1_2'
    SCORE_2_1 = 'score_2_1'
    SCORE_2_2 = 'score_2_2'
