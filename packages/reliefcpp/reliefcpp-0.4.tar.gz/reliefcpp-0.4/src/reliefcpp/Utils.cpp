#include "Utils.h"

namespace metric {

double euclidean_(const vector<double>& v1, const vector<double>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Vectors do not have the same size.");
    double sum = 0;
    for (size_t i = 0; i < v1.size(); ++i)
        sum += (v1[i] - v2[i]) * (v1[i] - v2[i]);
    return std::sqrt(sum);
}

double manhattan_(const vector<double>& v1, const vector<double>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Vectors do not have the same size.");
    double sum = 0;
    for (size_t i = 0; i < v1.size(); ++i)
        sum += std::abs(v1[i] - v2[i]);
    return sum;
}

double hamming_(const vector<double>& v1, const vector<double>& v2)
{
    if (v1.size() != v2.size())
        throw Exception("Vectors do not have the same size.");
    double sum = 0;
    for (size_t i = 0; i < v1.size(); ++i)
        sum += (v1[i] != v2[i]);
    return sum;
}

metric_enum metric_from_string(std::string name)
{
    if (name == "euclidean" || name == "l2")
        return euclidean;
    else if (name == "manhattan" || name == "l1")
        return manhattan;
    else if (name == "hamming")
        return hamming;
    else
        throw Exception("Metric has not been implemented.");
}

double compute(const vector<double>& v1, const vector<double>& v2, const metric_enum name)
{
    if (name == euclidean || name == l2)
        return euclidean_(v1, v2);
    else if (name == manhattan || name == l1)
        return manhattan_(v1, v2);
    else if (name == hamming)
        return hamming_(v1, v2);
    else
        throw Exception("Metric has not been implemented.");
}

}
