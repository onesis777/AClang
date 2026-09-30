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

long long min(const std::vector<long long>& a) {
    if (a.empty()) return 0;
    long long ret = a[0];
    for (auto x : a){
        ret = std::min(ret, x);
    }
    return ret;
}

long long max(const std::vector<long long>& a) {
    if (a.empty()) return 0;
    long long ret = a[0];
    for (auto x : a){
        ret = std::max(ret, x);
    }
    return ret;
}

int main(void) {
auto a = std::vector<long long>{1, 5, 6, 3, 0, 8, -1, -6, 10000000};
std::cout << std::boolalpha << min(a) << " " << max(a) << "\n";
return 0;
}