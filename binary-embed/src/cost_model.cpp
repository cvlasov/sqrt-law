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

#include <math.h>
#include <sstream>

#include "base_cost_model.h"
#include "base_cost_model_config.h"
#include "cost_model.h"
#include "cost_model_config.h"
#include "jstruct.h"
#include "mat2D.h"

cost_model::cost_model(
    jstruct* cover_struct, float* input_costs, cost_model_config* config)
    : base_cost_model(cover_struct, (base_cost_model_config*)config) {

  this->config = config;
  double wet_cost = (double)10000000000000;

  for (int row = 0; row < (int)cover_struct->image_height; row++) {
    for (int col = 0; col < (int)cover_struct->image_width; col++) {
      float rho = input_costs[col + row * cover_struct->image_width];

      // Cost of making a +1 change or a -1 change is the same, so we only need
      // to store one value. The cost is zero for making no change, so no need
      // to store that since it's constant.
      float* pixel_cost = costs + col + row * cover->cols;

      if (rho > wet_cost) {
        rho = wet_cost;
      }

      int cover_val = cover->Read(row, col);

      if (cover_val == -1023) {
        pixel_cost[0] = (float)wet_cost;
      } else {
        pixel_cost[0] = rho;
      }
    }
  }
}

cost_model::~cost_model() {}
