#include <iostream>
#include <string>
#include <algorithm>

int main() {
    int T = 0;
    std::cin >> T;
    while(T--) {
        std::string str;
        std::cin >> str;
        std::reverse(str.begin(), str.end());
        std::cout << str << std::endl;
    }
    return 0;
}
