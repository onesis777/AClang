#include <bits/stdc++.h>
using namespace std;

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

int main() {
cout << (((static_cast<long long>(((2 + 3) * 4)) / static_cast<long long>(2)) - static_cast<long long>(modpow(2, 5, 13)) % static_cast<long long>(3)) + intpow(2, pow(3, 2))) << endl;
}