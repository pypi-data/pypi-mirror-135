//
// This module defines the vanilla ReliefK variant.
// For each sample it averages the near misses and near hits scores.

#ifndef RELIEFK_H
#define RELIEFK_H

#include <cstddef> // size_t
#include <vector>

#include "AbstractVanillaRelief.h"
#include "Operations.h"

using std::vector;

class ReliefK : public AbstractVanillaRelief {
public:
    using AbstractVanillaRelief::AbstractVanillaRelief;
protected:
    // Vanilla ReliefK averages the neighbors
    Datapoint _process_neighbors(size_t id, const Dataset& X, const vector<size_t>& indices);
};

#endif // RELIEF_H