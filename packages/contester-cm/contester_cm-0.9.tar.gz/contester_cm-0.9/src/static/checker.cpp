#include "..\utils\testlib.h"

int main()
{
    registerTestlibCmd();

    int a = inf.readInteger();
    int b = inf.readInteger();

    int pattern = ouf.readLine();

    if (a + b != pattern) {
        quitf(_wa, "expected %d, found %d", pattern, a + b);
    }

    quitf(_ok, "answer is correct");
}

/*
registerTestlibCmd() - инициализация файлов inf, ouf, ans


inf - ввод с тестового файла input
ans - ввод с тестового файла output
ouf - ввод с файла вывода программы участника


.readInt()      - чтение int
.readLong()     - чтение long long
.readWord()     - чтение string
.readDouble()   - чтение double
.readLine()     - чтение строки с файла полностью


Чтение до конца файла:
while (!ouf.seekEof()) {}
*/