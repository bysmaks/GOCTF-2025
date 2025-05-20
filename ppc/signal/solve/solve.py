from pwn import *
from solver import Solver
from const import ADDR, PORT, MODEL_FILE

def main():
    solver = Solver()
    solver.load_model(MODEL_FILE)

    with remote(ADDR, PORT) as r:
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())
        print(r.recvline().decode())

        for attempt in range(1000):
            try:
                lvl_info = r.recvline().decode()
                print(lvl_info)

                # Парсим сигнал
                signal_json = r.recvline().decode()
                features = solver.parse_params(signal_json)

                # Предиктим
                prediction = solver.predict(features)

                # Отправляем ответ
                if prediction > 0.5:
                    r.sendline(b"ALIEN")
                else:
                    r.sendline(b"NOISE")

            except EOFError:
                print("Соединение закрыто")
                break
            except Exception as e:
                print(f"Критическая ошибка: {e}")
                break

        r.interactive()

if __name__ == "__main__":
    main()