from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    CONST_STRING: str = ('Тип тренировки: {training_type}; '
                         'Длительность: {duration:.3f} ч.; '
                         'Дистанция: {distance:.3f} км; '
                         'Ср. скорость: {speed:.3f} км/ч; '
                         'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить строку информационного сообщения."""
        return self.CONST_STRING.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed: float = self.get_distance() / self.duration
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Нужно реализовать get_spent_calories в '
                                  '%s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(type(self).__name__, self.duration,
                                   self.get_distance(), self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        duration_min: float = self.duration * 60
        spent_calories: float = ((coeff_calorie_1 * self.get_mean_speed()
                                 - coeff_calorie_2) * self.weight
                                 / self.M_IN_KM * duration_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при ходьбе."""
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        duration_min: float = self.duration * 60
        spent_calories: float = ((coeff_calorie_1 * self.weight
                                 + (self.get_mean_speed()**2 // self.height)
                                 * coeff_calorie_2 * self.weight)
                                 * duration_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        avg_speed: float = (self.length_pool * self.count_pool
                            / self.M_IN_KM / self.duration)
        return avg_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        coeff_calorie_1: float = 1.1
        spent_calories: float = ((self.get_mean_speed() + coeff_calorie_1)
                                 * 2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: dict = {'SWM': Swimming, 'RUN': Running,
                          'WLK': SportsWalking}
    training: Training = workout_dict[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    string: str = info.get_message()
    print(string)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
