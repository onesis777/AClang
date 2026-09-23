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

int main(void) {
auto N = []{ int n; std::cin >> n; return n; }();
auto T = [&]{
    std::vector<long long> _v(N);
    for (long long& _x : _v) std::cin >> _x;
    return _v;
}();
auto ti = std::vector<std::vector<long long>>();
for (long long i = 0; i < N; i += 1) {
ti.push_back(std::vector{T[i], (i + 1)});
}
std::sort(ti.begin(), ti.end());
std::cout << std::boolalpha << ti[0][1] << " " << ti[1][1] << " " << ti[2][1] << "\n";
return 0;
}