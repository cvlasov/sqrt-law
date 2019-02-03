#include "base_cost_model_config.h"

base_cost_model_config::base_cost_model_config(
    int payload_bits, bool verbose, int randSeed) {
	this->payload_bits = payload_bits;
	this->verbose = verbose;
	this->randSeed = randSeed;
}

base_cost_model_config::~base_cost_model_config() {}
