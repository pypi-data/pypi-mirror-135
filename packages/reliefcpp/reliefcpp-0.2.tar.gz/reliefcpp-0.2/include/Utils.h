#ifndef UTILS_H
#define UTILS_H

#include <algorithm>
#include <cmath>
#include <queue>
#include <random>
#include <string>
#include <vector>

#include "exceptions.h"

#ifdef DEBUG
#include <iostream>
using std::cout;
#endif

using std::vector;

namespace utils {

template <class RandomAccessIterator>
void shuffle(RandomAccessIterator begin, RandomAccessIterator end)
{
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(begin, end, g);
}

}

namespace metric {

double euclidean_(const vector<double>&, const vector<double>&);
double manhattan_(const vector<double>&, const vector<double>&);
double hamming_(const vector<double>&, const vector<double>&);

enum metric_enum {
    euclidean = 0,
    manhattan = 1,
    hamming = 2,
    l2 = 3,
    l1 = 4
};

metric_enum metric_from_string(std::string name);
double compute(const vector<double>& c1, const vector<double>& v2, const metric_enum name);

}

// Memory efficient DS that returns the top k elements
// according to some comparison object.
// If comparison object is std::greater, then will take the largest k
// otherwise, if std::less, will take the smallest k.
// Complexity n * log(k) where n is the total number of push-es.
template <class T, template <class> class Compare = std::less>
class TopKQueue {
public:
    TopKQueue(size_t k)
        : __k(k)
        , __comp(Compare<T>())
    {
        if (k < 1)
            throw Exception("k must be positive.");
        __pq = new std::priority_queue<T, vector<T>, Compare<T>>();
    }

    void push(T element)
    {
        if (__pq->size() < __k)
            __pq->push(element);
        else {
            if (__comp(element, __pq->top())) {
                __pq->pop();
                __pq->push(element);
            }
        }
    }

    vector<T> retrieve()
    {
        vector<T> result(__pq->size());
        size_t i = 0;
        while (!__pq->empty()) {
            result[i++] = __pq->top();
            __pq->pop();
        }
        return result;
    }

    size_t size() const
    {
        return __pq->size();
    }

private:
    const size_t __k;
    const Compare<T> __comp;
    std::priority_queue<T, vector<T>, Compare<T>>* __pq;
};

// Needed for sorting scores.
template <typename T>
vector<size_t> argsort(const vector<T>& v)
{
    vector<size_t> indices(v.size());
    std::iota(indices.begin(), indices.end(), 0);
    std::sort(indices.begin(), indices.end(),
        [&v](int left, int right) -> bool {
            return v[left] < v[right];
        });

    return indices;
}

#ifdef DEBUG
template <class T>
void print_vec(const vector<T>& v)
{
    for (size_t i = 0; i < v.size(); ++i)
        cout << v[i] << " ";
    cout << "\n";
}

template <class T>
void print_2dvec(const vector<vector<T>>& v)
{
    for (size_t i = 0; i < v.size(); ++i) {
        for (size_t j = 0; j < v[i].size(); ++j)
            cout << v[i][j] << " ";
        cout << "\n";
    }
}
#endif

#endif // UTILS_H