#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <tuple>

// 入出力の高速化
struct Init { Init() { std::ios::sync_with_stdio(0); std::cin.tie(0); } }init;

// x ^^ n のための繰り返し2乗法
long long intpow(long long x, long long n) {
    long long ret = 1;
    while (n > 0) {
        if (n & 1) ret *= x;
        x *= x;
        n >>= 1;
    }
    return ret;
}

// modpow のための繰り返し2乗法
long long modpow(long long x, long long n, long long MOD) {
    long long ret = 1;
    while (n > 0) {
        if (n & 1) ret = ret * x % MOD;
        x = x * x % MOD;
        n >>= 1;
    }
    return ret;
}

int main(void) {
long long A, B;
std::cin >> A >> B;
if ((15 <= (A + B)) && (8 <= B)) {
    std::cout << std::boolalpha << 1 << "\n";
} else if ((10 <= (A + B)) && (3 <= B)) {
    std::cout << std::boolalpha << 2 << "\n"; 
} else if (3 <= (A + B)) {
    std::cout << std::boolalpha << 3 << "\n"; 
} else {
    std::cout << std::boolalpha << 4 << "\n";
}
return 0;
}