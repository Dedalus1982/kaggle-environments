import random
from .utils import get_score

#Агент 1. Всегда выбирает 0 - камень
def rock_agent(observation, configuration):
    return 0

#Агент 2. Всегда выбирает 1 - бумага
def paper_agent(observation, configuration):
    return 1

#Агент 3. Всегда выбирает 2 - ножницы
def scissors_agent(observation, configuration):
    return 2

#Агент 4. Всегда выбирает случайное действие.
def randomme_agent(observation, configuration):
    from kaggle_environments import make, evaluate
    return random.randrange(0, 3)

#Агент 5. Производит то же самое действие, что и оппонент на прошлом ходу. На первом ходу - случаный выбор.
def copy_opponent(observation, configuration):
    #Если первый ход то идем рандомно
    if observation.step == 0:
        return random.randrange(0, configuration.signs)
    #На 2 и остальных ходах выбираем то что ход назад выбирал противник
    else:
        return observation.lastOpponentAction

#Агент 6. Производит случайно действия кроме того, что оппонент на прошлом ходу. На первом ходу - случаный выбор.
def not_copy_opponent(observation, configuration):
    #Если первый ход то идем рандомно
    if observation.step == 0:
        return random.randrange(0, configuration.signs)
    #На 2 и остальных ходах выбираем НЕ то что ход назад выбирал противник
    else:
        numbers = list(range(0, configuration.signs))
        # удаляем из списка действий то, которое призвел противник на прошлом ходу и случаной выбираем между оставшимся
        newnambers = numbers.remove(observation.lastOpponentAction)
        not_copy_opponent = random.choice(newnambers)
        return not_copy_opponent

#Агент 7. Производит действие, которое бы било прошлый выбор противника. На первом ходу - случаный выбор.
last_react_action = None
def reactionary(observation, configuration):
    global last_react_action
    # Если это первый шаг, задаем случайное действие
    if observation.step == 0:
        last_react_action = random.randrange(0, configuration.signs)
    # В остальных случаях, выбираем то что било бы прошлый выбор противника.
    else:
        last_react_action = (observation.lastOpponentAction + 1) % configuration.signs
    return last_react_action

#Агент 8. Не производит действие, которое бы било прошлый выбор противника. На первом ходу - случаный выбор.
last_react_action = None
def unreactionary(observation, configuration):
    global last_react_action
    # Если это первый шаг, задаем случайное действие
    if observation.step == 0:
        last_react_action = random.randrange(0, configuration.signs)
    # В остальных случаях, выбираем то что НЕ било бы прошлый выбор противника.
    else:
        numbers = list(range(0, configuration.signs))
        # удаляем из списка действий то, которое било бы противника на прошлом ходу и случаной выбираем между оставшимся
        newnambers = numbers.remove(observation.lastOpponentAction)
        last_react_action = random.choice(newnambers)
    return last_react_action

#Агент 9. Производит действие, которое:
# - если противник выиграл то выбирем то что мы били бы в прошлый раз,
# - в остальных случаях выбираем то что било бы противника в прошлый раз.
#На первом ходу - случаный выбор.
last_counter_action = None
def counter_reactionary(observation, configuration):
    global last_counter_action
    # Если это первый шаг, задаем случайное действие
    if observation.step == 0:
        last_counter_action = random.randrange(0, configuration.signs)
    # Узнаем, выиграл ли противник в прошлый раз
    elif get_score(last_counter_action, observation.lastOpponentAction) == 1:
        # Если противник выиграл то выбирем то что мы били бы в прошлый раз
        last_counter_action = (last_counter_action + 2) % configuration.signs
    # В остальных случаях выбираем то что било бы противника в прошлый раз
    else:
        last_counter_action = (observation.lastOpponentAction + 1) % configuration.signs
    return last_counter_action

# Агент 10. Производит действие, которое:
# - если противник выиграл то выбираем то что било бы противника в прошлый раз,
# - в остальных случаях выбирем то что мы били бы в прошлый раз.
# На первом ходу - случаный выбор.
last_uncounter_action = None
def uncounter_reactionary(observation, configuration):
    global last_uncounter_action
    # Если это первый шаг, задаем случайное действие
    if observation.step == 0:
        last_uncounter_action = random.randrange(0, configuration.signs)
    # Узнаем, выиграл ли противник в прошлый раз
    elif get_score(last_uncounter_action, observation.lastOpponentAction) == 1:
        last_uncounter_action = (observation.lastOpponentAction + 1) % configuration.signs
    else:
        last_uncounter_action = (last_uncounter_action + 2) % configuration.signs
    return last_uncounter_action

# Агент 11. Повторяет свой прошлый выбор, если в прошлый раз выиграл, если нет - рандом. На первом ходу - случаный выбор.
last_react_action = None
def repeat_if_win(observation, configuration):
    global last_react_action
    # Если это первый шаг, задаем случайное действие и возвращаем его
    if observation.step == 0:
        last_react_action = random.randrange(0, configuration.signs)
        return last_react_action
    # Проверяем результат предыдущего действия
    if get_score(last_react_action, observation.lastOpponentAction) > 0:
        # Если выиграли, повторяем то же действие
        return last_react_action
    else:
        # Если проиграли или ничья, выбираем новое случайное действие
        last_react_action = random.randrange(0, configuration.signs)
        return last_react_action

# Агент 12. Повторяет свой прошлый выбор, если в прошлый раз проиграл, если нет - рандом. На первом ходу - случаный выбор.
def repeat_if_lose(observation, configuration):
    global last_react_action
    # Если это первый шаг, задаем случайное действие и возвращаем его
    if observation.step == 0:
        last_react_action = random.randrange(0, configuration.signs)
        return last_react_action
    # Проверяем результат предыдущего действия
    if get_score(last_react_action, observation.lastOpponentAction) < 0:
        # Если проиграли, повторяем то же действие
        return last_react_action
    else:
        # Если выиграли или ничья, выбираем новое случайное действие
        last_react_action = random.randrange(0, configuration.signs)
        return last_react_action

# Агент 13. Перебирает на первом ходу камень, на втором - бумага, на третьем - ножницы, на четветом - камень, и так - по кругу
def zero_one_two(observation, configuration):
        return (observation.step + 2) % configuration.signs

# Агент 14. Перебирает на первом ходу камень, на втором - бумага, на третьем - ножницы, на четветом - камень, и так - по кругу.
# Когда выигрывает - повторяет что было в прошлый раз.

def repeat_if_win_or_zero_one_two(observation, configuration):
    last_react_action = 0
    # Для не первого шага:
    if observation.step > 0:
        # Проверяем результат предыдущего действия
        if get_score(last_react_action, observation.lastOpponentAction) > 0:
           # Если выиграли, повторяем то же действие
           return last_react_action
        else:
            # Если проиграли или ничья, выбираем новое случайное действие
            last_react_action = (observation.step + 2) % configuration.signs
    return last_react_action

agents = {
    "rock": rock_agent,
    "paper": paper_agent,
    "scissors": scissors_agent,
    "randomme": randomme_agent,
    "copy_opponent": copy_opponent,
    "not_copy_opponent": not_copy_opponent,
    "reactionary": reactionary,
    "unreactionary": reactionary,
    "counter_reactionary": counter_reactionary,
    "uncounter_reactionary": counter_reactionary,
    "repeat_if_win": repeat_if_win,
    "repeat_if_lose": repeat_if_lose,
    "zero_one_two": zero_one_two,
    "repeat_if_win_or_zero_one_two": repeat_if_win_or_zero_one_two,
}
