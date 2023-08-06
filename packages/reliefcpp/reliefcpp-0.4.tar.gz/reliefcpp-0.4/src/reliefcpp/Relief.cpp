#include "Relief.h"

Datapoint Relief::_process_neighbors(size_t id, const Dataset& X, const vector<size_t>& indices)
{
    // Average the points given by indices in X
    size_t n_points = indices.size();

    srand(time(NULL));
    size_t the_chosen_one = rand() % n_points;

    return pow(X[id] - X[indices[the_chosen_one]], 2);
}