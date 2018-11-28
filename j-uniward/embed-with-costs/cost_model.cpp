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
  double wetCost = (double)10000000000000;

  for (int row = 0; row < (int)cover_struct->image_height; row++) {
    for (int col = 0; col < (int)cover_struct->image_width; col++) {
      float rho = input_costs[col + row * cover_struct->image_width];

      // pixel_costs[0] is the cost of -1
      // pixel_costs[1] is the cost of no change
      // pixel_costs[2] is the cost of +1
      float* pixel_costs = costs + ((col + row * cover->cols) * 3);

      if (rho > wetCost) {
        rho = wetCost;
      }

      int coverVal = cover->Read(row, col);

      if (coverVal == -1023) {
        pixel_costs[0] = (float)wetCost;
      } else  {
        pixel_costs[0] = rho;
      }

      pixel_costs[1] = 0;

      if (coverVal == 1023) {
        pixel_costs[2] = (float)wetCost;
      } else {
        pixel_costs[2] = rho;
      }
    }
  }
}

cost_model::~cost_model() {}
