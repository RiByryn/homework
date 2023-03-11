import random
num = random.randint(1, 100)
print('Добро пожаловать в числовую угадайку!\nВведите число от 1 до 100:\n')


def is_valid(n):
    return n.isdigit() and 1 <= int(n) <= 100


def input_num():
    while True:
        guess = input()
        if is_valid(guess):
            return int(guess)
        else:
            print('А может быть все-таки введем целое число от 1 до 100?')


def compare_num():
    while True:
        n = input_num()
        if n < num:
            print('Ваше число меньше загаданного, попробуйте еще разок')
        elif n > num:
            print('Ваше число больше загаданного, попробуйте еще разок')
        else:
            print('Вы угадали, поздравляем!')
            break


compare_num()