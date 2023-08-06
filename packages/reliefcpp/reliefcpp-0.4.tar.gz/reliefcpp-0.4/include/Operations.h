#ifndef OPERATIONS_H
#define OPERATIONS_H

#include <vector>

#include "exceptions.h"

using std::vector;

template <class T>
vector<T> operator+(const vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot add vectors of differing sizes.");

    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] + v2[i];
    return vres;
}

template <class T, class C>
vector<T> operator+(const vector<T>& v1, C val)
{
    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] + val;
    return vres;
}

template <class T>
vector<T>& operator+=(vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot add vectors of differing sizes.");

    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] += v2[i];
    return v1;
}

template <class T, class C>
vector<T>& operator+=(vector<T>& v1, C val)
{
    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] += val;
    return v1;
}

template <class T>
vector<T> operator-(const vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot subtract vectors of differing sizes.");

    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] - v2[i];
    return vres;
}

template <class T, class C>
vector<T> operator-(const vector<T>& v1, C val)
{
    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] - val;
    return vres;
}

template <class T>
vector<T>& operator-=(vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot subtract vectors of differing sizes.");

    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] -= v2[i];
    return v1;
}

template <class T, class C>
vector<T>& operator-=(vector<T>& v1, C val)
{
    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] -= val;
    return v1;
}

template <class T>
vector<T> operator*(const vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot multiply vectors of differing sizes.");

    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] * v2[i];
    return vres;
}

template <class T, class C>
vector<T> operator*(const vector<T>& v1, C val)
{
    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] * val;
    return vres;
}

template <class T>
vector<T>& operator*=(vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot multiply vectors of differing sizes.");

    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] *= v2[i];
    return v1;
}

template <class T, class C>
vector<T>& operator*=(vector<T>& v1, C val)
{
    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] *= val;
    return v1;
}

template <class T>
vector<T> operator/(const vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot divide vectors of differing sizes.");

    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] / v2[i];
    return vres;
}

template <class T, class C>
vector<T> operator/(const vector<T>& v1, C val)
{
    if (val == 0)
        throw Exception("Cannot divide by 0.");

    vector<T> vres(v1.size());
    for (size_t i = 0; i < vres.size(); ++i)
        vres[i] = v1[i] / val;
    return vres;
}

template <class T>
vector<T>& operator/=(vector<T>& v1, const vector<T>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Cannot divide vectors of differing sizes.");

    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] /= v2[i];
    return v1;
}

template <class T, class C>
vector<T>& operator/=(vector<T>& v1, C val)
{
    if (val == 0)
        throw Exception("Cannot divide by 0.");
    for (size_t i = 0; i < v1.size(); ++i)
        v1[i] /= val;
    return v1;
}

template <class T>
T _fast_pow(T base, size_t power)
{
    // Small powers
    if (power == 2)
        return base * base;
    else if (power == 3)
        return base * base * base;

    T result = 1;
    while (power > 0) {
        if ((power & 1) == 1)
            result *= base;
        base *= base;
        power >>= 1;
    }
    return result;
}

template <class T>
vector<T> pow(const vector<T>& v, size_t power)
{
    vector<T> res(v.size());
    for (size_t i = 0; i < v.size(); ++i)
        res[i] = _fast_pow(v[i], power);
    return res;
}

#endif // OPERATIONS_H