//
// This module defines the vanilla Relief variant.
// For each sample it picks a random
// near miss and a random near hit and updates scores by computing the
// Euclidean distance between features.

#ifndef RELIEF_H
#define RELIEF_H

#include <cstddef> // size_t
#include <vector>
#include <stdlib.h> // rand

#include "AbstractVanillaRelief.h"
#include "Operations.h"

using std::vector;

class Relief : public AbstractVanillaRelief {
public:
    using AbstractVanillaRelief::AbstractVanillaRelief;
protected:
    // Vanilla Relief picks a random neighbor in a neighborhood
    // Setting n_neighbors to 1 effectively picks the nearest neighbor
    Datapoint _process_neighbors(size_t id, const Dataset& X, const vector<size_t>& indices);
};

#endif // RELIEF_H