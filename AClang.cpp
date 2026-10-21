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
#include <cassert>
#include <stdexcept>
#include <optional>

// オンラインジャッジでなければ配列外参照にエラーを出す
#ifndef ONLINE_JUDGE
#define _GLIBCXX_DEBUG
#endif

// 入出力の高速化
struct Init { Init() { std::ios::sync_with_stdio(0); std::cin.tie(0); } }init;

long long INF = 2e18;
long long MOD998 = 998244353;
long long MOD107 = 1000000007;

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

template <typename T>
decltype(auto) vector_access(const T& a, long long index) {
    long long n = static_cast<long long>(a.size());
    if (index < 0) index += n;
    assert(index >= 0 && "index out of range");
    return a[index];
}

template <typename T>
T slice(
    const T& a,
    std::optional<long long> start_arg,
    std::optional<long long> end_arg,
    long long step
) {
    if (step == 0) {
        throw std::invalid_argument("slice step cannot be zero");
    }

    T ret;
    long long n = static_cast<long long>(a.size());
    long long start, end;

    if (step > 0) {
        start = start_arg.value_or(0);
        end = end_arg.value_or(n);

        if (start_arg && start < 0) start += n;
        if (end_arg && end < 0) end += n;

        start = std::max(0LL, std::min(start, n));
        end = std::max(0LL, std::min(end, n));

        for (long long i = start; i < end; i += step) {
            ret.push_back(a[i]);
        }
    } else {
        start = start_arg.value_or(n - 1);
        end = end_arg.value_or(-1);

        if (start_arg && start < 0) start += n;
        if (end_arg && end < 0) end += n;

        start = std::max(-1LL, std::min(start, n - 1));
        end = std::max(-1LL, std::min(end, n - 1));

        for (long long i = start; i > end; i += step) {
            ret.push_back(a[i]);
        }
    }

    return ret;
}

int main(void) {
#line 1 "AClang.ac"
auto vec = std::vector<long long>{1, 2, 7, 0, 5};
#line 2 "AClang.ac"
auto v1 = slice(vec, 1, 3, 1);
#line 3 "AClang.ac"
for (auto&& x : v1) {
std::cout << std::boolalpha << x << " " << "";
}
#line 6 "AClang.ac"
std::cout << std::boolalpha << "" << "\n";
#line 7 "AClang.ac"
std::cout << std::boolalpha << vector_access(vec, -1) << "\n";
#line 8 "AClang.ac"
auto v2 = slice(vec, std::nullopt, std::nullopt, -1);
#line 9 "AClang.ac"
for (auto&& x : v2) {
std::cout << std::boolalpha << x << " " << "";
}
#line 12 "AClang.ac"
std::cout << std::boolalpha << "" << "\n";
return 0;
}