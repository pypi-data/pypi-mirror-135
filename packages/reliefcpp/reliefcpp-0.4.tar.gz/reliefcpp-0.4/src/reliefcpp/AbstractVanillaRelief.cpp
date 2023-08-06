#include "Relief.h"

AbstractVanillaRelief::AbstractVanillaRelief(size_t n_iter, size_t n_jobs, size_t n_neighbors, metric_enum name)
    : AbstractRelief(n_iter, n_jobs, name)
    , __n_neighbors(n_neighbors)
{
}

void AbstractVanillaRelief::_process_sample(size_t id, const Dataset& X, const Labels& y, vector<double>& scores)
{
    // Initialize memory-efficient queues that will store
    // top k nearest neighbors for each class.
    // Queue may be smaller if there are less points than __n_neighbors.
    TopKQueue<pair<double, size_t>> tkq_near_hits(__n_neighbors);
    TopKQueue<pair<double, size_t>> tkq_near_miss(__n_neighbors);
    for (size_t i = 0; i < X.size(); ++i) {
        if (i == id)
            continue;
        auto dist = this->dist(X[id], X[i]);
        if (y[i] == y[id])
            tkq_near_hits.push({ dist, i });
        else
            tkq_near_miss.push({ dist, i });
    }

    // Obtain the nearest neighbors for each class
    vector<pair<double, size_t>> p_near_hits = tkq_near_hits.retrieve();
    vector<pair<double, size_t>> p_near_miss = tkq_near_miss.retrieve();
    // Obtain the indices of the nearest neighbors
    vector<size_t> near_hits = this->__extract_id_from_pair(p_near_hits);
    vector<size_t> near_miss = this->__extract_id_from_pair(p_near_miss);
    // Average the neighbors belonging to a class
    if (!near_hits.empty()) {
        Datapoint near_hits_score = this->_process_neighbors(id, X, near_hits);
        scores -= near_hits_score;
    }
    if (!near_miss.empty()) {
        Datapoint near_miss_score = this->_process_neighbors(id, X, near_miss);
        scores += near_miss_score;
    }
}

vector<size_t> AbstractVanillaRelief::__extract_id_from_pair(const vector<pair<double, size_t>>& v)
{
    // Assuming a vector of pair<distance, index>
    // extract index from it
    vector<size_t> extracted(v.size());
    for (size_t i = 0; i < v.size(); ++i)
        extracted[i] = v[i].second;
    return extracted;
}
