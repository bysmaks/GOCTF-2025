#include <iostream>
#include <vector>
#include <string>
#include <cstring>
#include <cstdint>

// 1_0-2_1-2_2-1_3-1_4-2_5-2_6-1_7-3_3_0-3_3_0-3_3_0-3_3_1-3_3_1-3_3_1-3_3_1-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_2-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_3-3_3_5-3_3_5-3_3_5-3_3_5-3_3_5-3_3_6-3_3_6-3_3_6-3_3_6-3_3_6-3_3_6-3_3_7-3_3_7-3_3_7-3_3_7-3_3_7-3_3_7-3_3_7-52

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::string prog = argv[1];
    std::vector<uint8_t> reg(8, 0); // "регистр" для пароля

    // Эталонная строка зашифрована цезарем -1
    char enc[] = { 'i','K','Y','{','c','M','O','q',0 };
    char ref[9];
    for (int i = 0; i < 8; ++i) ref[i] = enc[i] - 1;
    ref[8] = 0;

    size_t pos = 0;
    while (pos < prog.size()) {
        // Найти следующую инструкцию (разделитель -)
        size_t next = prog.find('-', pos);
        std::string instr = prog.substr(pos, next - pos);
        // Обфусцированное сравнение с "52"
        if (instr.size() == 2 && (instr[0] ^ 7) == ('5' ^ 7) && (instr[1] ^ 7) == ('2' ^ 7)) {
            if (memcmp(reg.data(), ref, 8) == 0) return 0;
            else return 1;
        } else if (instr.size() == 3 && instr[1] == '_') {
            int cmd = instr[0] - '0';
            int idx = instr[2] - '0';
            if (cmd == 1 && idx >= 0 && idx < 8) reg[idx] = 'b';
            else if (cmd == 2 && idx >= 0 && idx < 8) reg[idx] = 'B';
        } else if (instr.size() == 5 && instr[0] == '3' && instr[1] == '_' && instr[2] == '3' && instr[3] == '_') {
            int idx = instr[4] - '0';
            if (idx >= 0 && idx < 8) reg[idx] += 2;
        }
        // Следующая инструкция
        if (next == std::string::npos) break;
        pos = next + 1;
    }
    return 1;
}
