from app.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """Запуск игры"""
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        """
        Проверка здоровья игрока и противника.
        Расчет результатов битвы (Ничья, Победа, Проигрыш).
        """
        if self.player.hp > 0 and self.enemy.hp > 0:
            return None

        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        self.battle_result = "Игрок проиграл" if self.player.hp <= 0 else "Игрок выиграл"

        return self._end_game()

    def _stamina_regeneration(self):
        """Регенерация здоровья и стамины для игрока и врага за ход"""

        self.player.stamina = min(self.player.stamina + self.STAMINA_PER_ROUND, self.player.unit_class.max_stamina)
        self.enemy.stamina = min(self.enemy.stamina + self.STAMINA_PER_ROUND, self.enemy.unit_class.max_stamina)

    def next_turn(self):
        """Следующий ход"""

        result = self._check_players_hp()
        if result is not None:
            return result

        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self):
        """Остановка игры"""

        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        """Удар игрока"""

        result = self.player.hit(self.enemy)
        turn_result = self.next_turn()
        return f"{result}<br>{turn_result}"

    def player_use_skill(self):
        """Использование умения игрока"""

        result = self.player.use_skill(self.enemy)
        turn_result = self.next_turn()
        return f"{result}<br>{turn_result}"
