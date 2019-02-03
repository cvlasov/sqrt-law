#include <algorithm>
#include <iostream>
#include <limits>
#include <math.h>
#include <memory.h>
#include <string>
#include <time.h>
#include <valarray>

#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/uniform_real.hpp>
#include <boost/random/variate_generator.hpp>

#include "base_cost_model.h"
#include "exception.hpp"
#include "info_theory.h"
#include "mat2D.h"
#include "mi_embedder.h"

typedef unsigned int uint;
typedef std::valarray<float> va_float;

// MUTUALLY INDEPENDENT EMBEDDING ALGORITHM

int choose_coefficient_change(float change_prob, double rand1, double rand2) {
	if (rand1 < change_prob) {
    if (rand2 < 0.5) {
      return 1;
    } else {
      return -1;
    }
  } else {
    return 0;
  }
}

float cost_to_probability(float change_cost, float lambda) {
	return 1 / (1 + exp(lambda * change_cost));
}

float entropy(float change_prob) {
  if (change_prob > exp(-10)) {
    return - change_prob * log2f(change_prob)
           - (1-change_prob) * log2f(1-change_prob);
  } else {
    return 0;
  }
}

float compute_entropy_sum(base_cost_model* m, float lambda) {
  float entropy_sum = 0;

  for (int i = 0; i < m->rows; i++) {
    for (int j = 0; j < m->cols; j++) {
      float change_cost = (m->costs + i * m->cols + j)[0];
      float change_prob = cost_to_probability(change_cost, lambda);
      entropy_sum += entropy(change_prob);
    }
  }

  return entropy_sum;
}

mat2D<int>* simulate_pls_embedding(
    base_cost_model* m, int payload_bits, uint seed, float& distortion) {
  float lambda = calculate_lambda_from_payload(m, payload_bits);

	mat2D<int>* stego = new mat2D<int>(m->rows, m->cols);
  boost::mt19937 generator(seed);
  boost::variate_generator<boost::mt19937&, boost::uniform_real<> >
      rng(generator, boost::uniform_real<>(0,1));

  for (int i = 0; i < m->rows; i++) {
    for (int j = 0; j < m->cols; j++) {
	    float change_cost = (m->costs + i * m->cols + j)[0];
	    float change_prob = cost_to_probability(change_cost, lambda);
      int coef_change = choose_coefficient_change(change_prob, rng(), rng());
	    stego->Write(i, j, m->cover->Read(i,j) + coef_change);

      // Update distortion
      if (coef_change == -1 || coef_change == 1) {
        distortion += change_cost;
      } // else distortion += 0 since not making a change has cost zero
    }
  }

  return stego;
}

float calculate_lambda_from_payload(
    base_cost_model* m, int payload_bits) {
  float lambda = 0;
  float lower_bound = -1;
  float upper_bound = -1;

  // Exponential search for an upper and lower bound on lambda
  while (true) {
    float entropy_sum = compute_entropy_sum(m, lambda);

    if (entropy_sum < payload_bits) {
      lower_bound = lambda == 1 ? 0 : (lambda/10);
      upper_bound = lambda;
      break;
    }

    lambda = lambda == 0 ? 1 : (lambda*10);
  }

  // Binary search to find lambda such that the sum of the entropies of each
  // probability of change is >= the number of payload bits and < the number of
  // payload bits + 2

  // This "error" factor is necessary due to a lack of floating-point precision
  // during the binary search. The entropy sum may never be able to reach the
  // range [bits...bits+1), so this requirement is relaxed a bit.
  int error = 2;

  while (lower_bound <= upper_bound) {
    lambda = (upper_bound + lower_bound) / 2;
    float entropy_sum = compute_entropy_sum(m, lambda);

    if (payload_bits <= entropy_sum && entropy_sum < payload_bits + error) {
      break;
    } else if (entropy_sum < payload_bits) {
      upper_bound = lambda;
    } else {
      lower_bound = lambda;
    }
  }

  return lambda;
}
