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
