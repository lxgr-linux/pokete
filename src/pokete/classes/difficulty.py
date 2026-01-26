import math


class DifficultyManager:
    """
    Manages the dynamic difficulty scaling of the game.
    Uses an Exponential Moving Average (EMA) of player performance.
    """

    MIN_SCORE = 0.5
    MAX_SCORE = 2.0
    ALPHA = 0.25  # Smoothing factor for EMA (higher is more reactive)

    def __init__(self, data=None):
        self.score = 1.0
        self.history = []
        if data:
            self.from_dict(data)

    def record_battle(self, won, player_hp_pct, player_lvl, enemy_lvl, turns):
        """
        Calculates a Performance Rating for the battle and updates the EMA score.
        ARGS:
            won: bool, whether the player won the battle.
            player_hp_pct: float (0.0 to 1.0), remaining HP of the player's active team.
            player_lvl: int, average level of the player's team.
            enemy_lvl: int, average level of the enemy team.
            turns: int, total number of turns the battle took.
        """
        # Base rating from win/loss
        # A standard win is 1.1 (slightly above difficulty 1.0)
        # A standard loss is 0.6
        base_rating = 1.15 if won else 0.6

        # Adjust for HP remaining (if won)
        # If won with 100% HP, +0.15. If won with 0% HP (last poke standing), -0.15.
        hp_bonus = (player_hp_pct - 0.5) * 0.3 if won else 0

        # Adjust for Level Gap
        # If you win against higher lvl, rating goes up.
        # If you lose against lower lvl, rating goes down.
        lvl_ratio = enemy_lvl / max(player_lvl, 1)
        # log2(1) = 0, log2(2) = 1, log2(0.5) = -1.
        # We want ratio 1 to be factor 1.0.
        lvl_factor = math.log2(lvl_ratio + 1)

        # Adjust for efficiency (Turn count)
        # Average battle is assumed to be around 8 turns.
        # 4 turns is very efficient (+0.1), 16 turns is slow (-0.1).
        turn_factor = 1.0 + (8 - max(4, min(turns, 20))) * 0.025

        performance_rating = (base_rating + hp_bonus) * lvl_factor * turn_factor

        # Update Score using EMA
        # score = (alpha * current_rating) + ((1 - alpha) * old_score)
        self.score = (self.ALPHA * performance_rating) + (
            (1 - self.ALPHA) * self.score
        )

        # Elasticity: Subtle pull back towards 1.0 to prevent runaway difficulty
        # over long periods of extreme performance.
        self.score = (0.97 * self.score) + (0.03 * 1.0)

        # Final Clamp to ensure values remain within sane bounds
        self.score = max(self.MIN_SCORE, min(self.MAX_SCORE, self.score))

        # Record history for transparency (max 10 entries)
        self.history.append(
            {
                "won": won,
                "hp_pct": round(player_hp_pct, 2),
                "lvl_ratio": round(lvl_ratio, 2),
                "turns": turns,
                "rating": round(performance_rating, 2),
                "new_score": round(self.score, 2),
            }
        )
        if len(self.history) > 10:
            self.history.pop(0)

    def get_stat_multiplier(self):
        """Returns a multiplier for enemy stats (Atc, Def, Init)."""
        return round(self.score, 2)

    def get_level_offset(self):
        """Returns a level offset for encounters (e.g. -3 to +5)."""
        if self.score >= 1.0:
            # Score 2.0 -> +5 levels
            return round((self.score - 1.0) * 5)
        else:
            # Score 0.5 -> -3 levels
            return round((self.score - 1.0) * 6)

    def to_dict(self):
        """Serializes the state for saving."""
        return {"score": self.score, "history": self.history}

    def from_dict(self, data):
        """Deserializes the state from a save file."""
        if not data:
            return
        self.score = data.get("score", 1.0)
        self.history = data.get("history", [])
