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

// オンラインジャッジでなければ配列外参照にエラーを出す
#ifndef ONLINE_JUDGE
#define _GLIBCXX_DEBUG
#endif

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

template <typename T>
T min(const std::vector<T>& a) {
    if (a.empty()) return 0;

    T ret = a[0];
    for (auto x : a) {
        ret = std::min(ret, x);
    }
    return ret;
}

template <typename T>
T max(const std::vector<T>& a) {
    if (a.empty()) return 0;

    T ret = a[0];
    for (auto x : a) {
        ret = std::max(ret, x);
    }
    return ret;
}

template <typename T>
T sum(const std::vector<T>& a) {
    T total = 0;
    for (T x : a) {
        total += x;
    }
    return total;
}

template <typename T>
bool chmax(T &a, const T& b) {
    if (a < b) {
        a = b;
        return true;
    }
    return false;
}

template <typename T>
bool chmin(T &a, const T& b) {
    if (a > b) {
        a = b;
        return true;
    }
    return false;
}

int main(void) {
long long a;
long long b;
long long c;
long long x;
std::cin >> a >> b >> c >> x;
auto ans = 0;
for (long long i = 0; i < (a + 1); i++) {
for (long long j = 0; j < (b + 1); j++) {
for (long long k = 0; k < (c + 1); k++) {
if (((((500 * i) + (100 * j)) + (50 * k)) == x)) {
    ans++;
} 
}

}

}

std::cout << std::boolalpha << ans << "\n";
return 0;
}