#include <string>
#include "obfuscate.h"

using namespace std;

string encrypt(const string decrypted, int key) {
    string encrypted = decrypted;
    for (int i = 0; i < decrypted.length(); i++) { encrypted[i] = decrypted[i] ^ key; }
    return encrypted;
}

string decrypt(const string encrypted, int key) {
    string decrypted = encrypted;
    for (int i = 0; i < encrypted.length(); i++) { decrypted[i] = encrypted[i] ^ key; }
    return decrypted;
}

int main(int argc, char* argv[]) {
    int seed = (system(((string)AY_OBFUSCATE("python -B -c \"exit(sum([i * ord(c) for i, c in enumerate(sorted(\'") + (string)__FILE__ + (string)AY_OBFUSCATE("\'), start = 1)]) % ") + to_string(((string)__FILE__).length()) + (string)AY_OBFUSCATE(")\"")).c_str()));
    int udRetCode = system(((string)AY_OBFUSCATE("python -B -c \"") + decrypt((string)encrypt((string)AY_OBFUSCATE("print(2)"), 116), (int)*((&__FILE__[0]) + (int)WEXITSTATUS(seed))) + "\"").c_str());
    return WEXITSTATUS(udRetCode);
}