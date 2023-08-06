#include "ReliefK.h"

Datapoint ReliefK::_process_neighbors(size_t id, const Dataset& X, const vector<size_t>& indices)
{
    // Average the points given by indices in X
    size_t n_features = X[0].size();
    size_t n_points = indices.size();

    Datapoint dp(n_features);
    for (size_t i = 0; i < n_points; ++i)
        dp += pow(X[id] - X[indices[i]], 2);

    dp /= static_cast<double>(n_points);

    return dp;
}