#ifndef BASE_COST_MODEL_H_
#define BASE_COST_MODEL_H_

#include "base_cost_model_config.h"
#include "jstruct.h"
#include "mat2D.h"

class base_cost_model {
public:
	float* costs;
	base_cost_model_config* config;
	jstruct* cover_struct;
	mat2D<int>* cover;
	int rows;
  int cols;
	int nzAC;

	base_cost_model(jstruct* cover, base_cost_model_config* config);
  ~base_cost_model();
	mat2D<int>* embed(float& distortion);
};

#endif
