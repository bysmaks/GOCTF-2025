import json

from const import PORT, TRAIN_FILE, TEST_FILE, ADDR
from pwn import *
from solver import Solver
from random import random

solver = Solver()
x_train = []
y_train = []
x_test = []
y_test = []


print("Собираем трейн сет...")
for i in range(5):
    with remote(ADDR, PORT) as r:
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())

        print(r.recvline().decode())
        prev_correct = 0

        for attempt in range(999):
            if attempt % 100 == 0:
                print(f"Собрано: train ({len(x_train)}), test ({len(x_test)})")

            try:
                signal_json = r.recvline().decode()
                # Парсим параметры сигнала
                features = solver.parse_params(signal_json)

                # Отправляем ответ ALIEN
                r.sendline(f"ALIEN".encode("utf-8"))

                # Получаем метрики (i и correct)
                lvl_info = r.recvline().decode()

                # Вытаскиваем correct
                correct = int(lvl_info.split("=")[2].split("]")[0].strip())

                # Если новый correct отличается от предыдущего, значит ответ ALIEN был верным
                # и мы сохранением метку 1.0, иначе 0.0.
                y = 1.0 if prev_correct < correct else 0.0
                prev_correct = correct

                # Сохраняем данные: 20% - test, 80% - train
                if random() < 0.2:
                    x_test.append(features)
                    y_test.append(y)
                else:
                    x_train.append(features)
                    y_train.append(y)

            except EOFError:
                print("Соединение закрыто")
                break
            except Exception as e:
                print(f"Критическая ошибка: {e}")
                break

print(f"Собрано: train ({len(x_train)}), test ({len(x_test)})")

with open(TRAIN_FILE, "w") as f:
    f.write(json.dumps({"x": x_train, "y": y_train}))

with open(TEST_FILE, "w") as f:
    f.write(json.dumps({"x": x_test, "y": y_test}))

print(f"train data saved in '{TRAIN_FILE}'")
print(f"test data saved in '{TEST_FILE}'")