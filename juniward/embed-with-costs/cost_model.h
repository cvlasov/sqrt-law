/*
-------------------------------------------------------------------------
Copyright (c) 2013 DDE Lab, Binghamton University, NY.
All Rights Reserved.
-------------------------------------------------------------------------
Permission to use, copy, modify, and distribute this software for
educational, research and non-profit purposes, without fee, and without a
written agreement is hereby granted, provided that this copyright notice
appears in all copies. The program is supplied "as is," without any
accompanying services from DDE Lab. DDE Lab does not warrant the
operation of the program will be uninterrupted or error-free. The
end-user understands that the program was developed for research purposes
and is advised not to rely exclusively on the program for any reason. In
no event shall Binghamton University or DDE Lab be liable to any party
for direct, indirect, special, incidental, or consequential damages,
including lost profits, arising out of the use of this software. DDE Lab
disclaims any warranties, and has no obligations to provide maintenance,
support, updates, enhancements or modifications.
-------------------------------------------------------------------------
Original contact: vojtech_holub@yahoo.com | fridrich@binghamton.edu |
February 2013
         http://dde.binghamton.edu/download/stego_algorithms/
-------------------------------------------------------------------------
*/

#ifndef COST_MODEL_H_
#define COST_MODEL_H_

#include <vector>

#include "base_cost_model.h"
#include "cost_model_config.h"
#include "jstruct.h"
#include "mat2D.h"

class cost_model : public base_cost_model {
public:
  cost_model(jstruct* cover_struct, float* input_costs,
             cost_model_config* config);
  ~cost_model();

private:
  cost_model_config* config;

  void calc_costs(int r, int c, mat2D<int>* cover_padded, float* pixel_costs);
  void eval_direction(int i, int j, int dir_i, int dir_j,
                      mat2D<int>* cover_padded, float* pixel_costs);
  float eval_cost(int k, int l, int m);
};

#endif
