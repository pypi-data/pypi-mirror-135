#include "ReliefF.h"

void ReliefF::_verify_labels(const Labels& y)
{
    __prior_p.clear();
    for (size_t i = 0; i < y.size(); ++i)
        ++__prior_p[y[i]];
    for (auto it = __prior_p.begin(); it != __prior_p.end(); ++it)
        it->second /= static_cast<double>(y.size());
}

void ReliefF::_process_sample(size_t id, const Dataset& X, const Labels& y, vector<double>& scores)
{
    // <Class label, <sample index, distance to id>
    map<Label, pair<size_t, double>> neighbors;
    map<Label, pair<size_t, double>>::iterator it;
    double distance_to_i;

    for (size_t i = 0; i < X.size(); ++i) {
        if (i == id)
            continue;
        it = neighbors.find(y[i]);
        distance_to_i = this->dist(X[id], X[i]);
        if (it == neighbors.end()) { // If no sample of this class has been seen so far
            neighbors[y[i]] = { i, distance_to_i };
        } else if ((it->second).second > distance_to_i) { // Check if this sample if closer than its friend
            (it->second).first = i;
            (it->second).second = distance_to_i;
        }
    }

    // Consider each nearest neghbor from every class and update
    // the score accordingly.
    for (auto ut = neighbors.begin(); ut != neighbors.end(); ++ut) {
        if (ut->first == y[id]) // Near hit
            scores -= pow(X[id] - X[(ut->second).first], 2);
        else // Neighbor from other class, scale by prior probability
            scores += pow(X[id] - X[(ut->second).first], 2) * __prior_p[ut->first];
    }
}