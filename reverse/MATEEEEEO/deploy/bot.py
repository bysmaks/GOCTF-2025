import telebot
import subprocess
import threading
import time

BIN_TIMEOUT = 5  # секунд на выполнение бинарника
BIN_COOLDOWN = 5 # минимальный интервал между запусками бинаря (секунд)
MAX_PASS_LEN = 430

user_limits = {}  # user_id: {'last': timestamp}

def run_binary_limited(user_id, cmd, input_arg):
    now = time.time()
    lim = user_limits.setdefault(user_id, {'last': 0})
    if now - lim['last'] < BIN_COOLDOWN:
        return None, f"Запускать можно не чаще, чем раз в {BIN_COOLDOWN} секунд."
    lim['last'] = now

    result = {'proc': None}
    def target():
        try:
            result['proc'] = subprocess.run(cmd, capture_output=True, timeout=BIN_TIMEOUT)
        except Exception:
            result['proc'] = None

    t = threading.Thread(target=target)
    t.start()
    t.join(BIN_TIMEOUT + 1)
    if t.is_alive():
        return None, "Время ожидания истекло. Попробуйте снова."
    return result['proc'], None

with open('api.txt') as f:
    API_KEY = f.read().strip()

bot = telebot.TeleBot(API_KEY)

user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_limits[message.chat.id] = {'last': 0}
    bot.send_message(message.chat.id, "Введите имя:")
    user_states[message.chat.id] = {'step': 'name'}

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('step') == 'name')
def handle_name(message):
    name = message.text.strip()
    proc, err = run_binary_limited(message.chat.id, ['./checker_go', name], name)
    if err or proc is None or proc.returncode != 0:
        bot.send_message(message.chat.id, "Неверное имя или ошибка. Попробуйте снова.")
        user_states[message.chat.id] = {'step': 'name'}
        return
    with open('part1.txt') as f:
        part1 = f.read().strip()
    bot.send_message(message.chat.id, f"Часть 1 ключа: {part1}\nТеперь введите пароль:")
    user_states[message.chat.id] = {'step': 'password'}

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('step') == 'password')
def handle_password(message):
    password = message.text.strip()
    if len(password) > MAX_PASS_LEN:
        bot.send_message(message.chat.id, f"Пароль слишком длинный (максимум {MAX_PASS_LEN} символов). Введите имя заново.")
        user_states[message.chat.id] = {'step': 'name'}
        return
    proc, err = run_binary_limited(message.chat.id, ['./checker_cpp_upx', password], password)
    if err or proc is None or proc.returncode != 0:
        bot.send_message(message.chat.id, "Неверный пароль или ошибка. Введите имя заново.")
        user_states[message.chat.id] = {'step': 'name'}
        return
    with open('part2.txt') as f:
        part2 = f.read().strip()
    bot.send_message(message.chat.id, f"Часть 2 ключа: {part2}\nТеперь отправьте ключ для получения флага:")
    user_states[message.chat.id] = {'step': 'key'}

@bot.message_handler(func=lambda m: user_states.get(m.chat.id, {}).get('step') == 'key')
def handle_key(message):
    user_key = message.text.strip()
    with open('key.txt') as f:
        real_key = f.read().strip()
    if user_key == real_key:
        with open('flag.txt') as f:
            flag = f.read().strip()
        bot.send_message(message.chat.id, f"Флаг: {flag}")
        user_states[message.chat.id] = {'step': 'done'}
    else:
        bot.send_message(message.chat.id, "Неверный ключ. Попробуйте снова.")

bot.polling()