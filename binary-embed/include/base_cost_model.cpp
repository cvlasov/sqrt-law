#include "base_cost_model.h"
#include "base_cost_model_config.h"
#include "jstruct.h"
#include "mat2D.h"
#include "mi_embedder.h"

#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/variate_generator.hpp>

base_cost_model::base_cost_model(jstruct* cover_struct,
                                 base_cost_model_config* config) {
	this->cover_struct = cover_struct;
	this->cover = cover_struct->coef_arrays[0];
	this->rows = cover_struct->image_height;
	this->cols = cover_struct->image_width;
	this->config = config;
	this->costs = new float[this->rows * this->cols];
	this->nzAC = 0;

  // Count the number of non-zero coefficients
	for (int row = 0; row < this->rows; row++) {
		for (int col = 0; col < this->cols; col++) {
			if (!((row % 8 == 0) && (col % 8 == 0))
          && (this->cover->Read(row, col) != 0)) {
				this->nzAC++;
      }
    }
  }
}

base_cost_model::~base_cost_model() {
	delete this->costs;
}

mat2D<int>* base_cost_model::embed(float& distortion) {
	boost::mt19937 generator(this->config->randSeed);
  boost::variate_generator<boost::mt19937&, boost::uniform_int<> > rng(
      generator, boost::uniform_int<>(0, RAND_MAX));
	return simulate_pls_embedding(this, config->payload_bits, rng(), distortion);
}
