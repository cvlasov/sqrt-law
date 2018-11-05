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
    jstruct* coverStruct, cost_model_config* config, const char* filename)
    : base_cost_model(coverStruct, (base_cost_model_config*)config) {

	this->config = config;
	double wetCost = (double)10000000000000;
	mat2D<int>* spatialCover = coverStruct->spatial_arrays[0];

	// Adjust wavelet impact to the quality factor
	mat2D<mat2D<double>*>* LHwaveletImpact = new mat2D<mat2D<double>*>(8, 8);
	mat2D<mat2D<double>*>* HLwaveletImpact = new mat2D<mat2D<double>*>(8, 8);
	mat2D<mat2D<double>*>* HHwaveletImpact = new mat2D<mat2D<double>*>(8, 8);

	for (int row = 0; row < 8; row++) {
		for (int col = 0; col < 8; col++) {
			int quant = coverStruct->quant_tables[0]->Read(row, col);

			LHwaveletImpact->Write(row, col,
				mat2D<double>::ChangeToAbsValue(
					mat2D<double>::MultiplyByNumber(
						config->LHwaveletImpact->Read(row, col), quant)));

			HLwaveletImpact->Write(row, col,
				mat2D<double>::ChangeToAbsValue(
					mat2D<double>::MultiplyByNumber(
						config->HLwaveletImpact->Read(row, col), quant)));

			HHwaveletImpact->Write(row, col,
				mat2D<double>::ChangeToAbsValue(
					mat2D<double>::MultiplyByNumber(
						config->HHwaveletImpact->Read(row, col), quant)));
		}
	}

	// Create padded image
	mat2D<int>* spatialCover_padded_int =
	  mat2D<int>::Padding_Mirror(spatialCover, config->padsize, config->padsize);

	mat2D<double>* spatialCover_padded_double =
	  mat2D<double>::Retype_int2double(spatialCover_padded_int);

	delete spatialCover_padded_int;

	// Compute residuals - wavelet sub-bands
	mat2D<double>* R_LH =
	  mat2D<double>::ChangeToAbsValue(
			mat2D<double>::Correlation_Same_basicFilters(
				spatialCover_padded_double, config->Tlpdf, config->hpdf));

	mat2D<double>* R_HL =
	  mat2D<double>::ChangeToAbsValue(
			mat2D<double>::Correlation_Same_basicFilters(
				spatialCover_padded_double, config->Thpdf, config->lpdf));

	mat2D<double>* R_HH =
	  mat2D<double>::ChangeToAbsValue(
			mat2D<double>::Correlation_Same_basicFilters(
				spatialCover_padded_double, config->Thpdf, config->hpdf));

	delete spatialCover_padded_double;

	for (int row = 0; row < (int)coverStruct->image_height; row++) {
		for (int col = 0; col < (int)coverStruct->image_width; col++) {
			int modRow = row % 8;
			int modCol = col % 8;

			int subRowsFrom = row - modRow - 6 + config->padsize;
			int subColsFrom = col - modCol - 6 + config->padsize;

			double rho = 0;

      for (int r_sub = 0; r_sub < 7 + config->padsize; r_sub++) {
				for (int c_sub = 0; c_sub < 7 + config->padsize; c_sub++) {
					rho += LHwaveletImpact->Read(modRow, modCol)->Read(r_sub, c_sub) /
					  (R_LH->Read(subRowsFrom+r_sub, subColsFrom+c_sub) + config->sigma);

					rho += HLwaveletImpact->Read(modRow, modCol)->Read(r_sub, c_sub) /
					  (R_HL->Read(subRowsFrom+r_sub, subColsFrom+c_sub) + config->sigma);

					rho += HHwaveletImpact->Read(modRow, modCol)->Read(r_sub, c_sub) /
					  (R_HH->Read(subRowsFrom+r_sub, subColsFrom+c_sub) + config->sigma);
				}
      }

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
				pixel_costs[0] = (float)rho;
			}

			pixel_costs[1] = 0;

			if (coverVal == 1023) {
				pixel_costs[2] = (float)wetCost;
			} else {
				pixel_costs[2] = (float)rho;
			}
		}
	}

	delete R_LH;
	delete R_HL;
	delete R_HH;
}

cost_model::~cost_model() {}
