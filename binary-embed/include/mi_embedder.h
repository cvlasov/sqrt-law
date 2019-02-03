#ifndef MI_EMBEDDER_H_
#define MI_EMBEDDER_H_

#include <cfloat>

#include "base_cost_model.h"
#include "exception.hpp"
#include "mat2D.h"

typedef unsigned int uint;

// MUTUALLY INDEPENDENT EMBEDDING ALGORITHM

mat2D<int>* simulate_pls_embedding(base_cost_model* m, int payload_bits,
                                   uint seed, float& distortion);
float calculate_lambda_from_payload(base_cost_model* m, int payload_bits);

#endif // MI_EMBEDDER_H_
