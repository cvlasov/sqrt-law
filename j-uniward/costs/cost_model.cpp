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
#include "time.h"

cost_model::cost_model(
    jstruct* coverStruct, cost_model_config* config, const char* filename)
    : base_cost_model(coverStruct, (base_cost_model_config*)config) {

  this->config = config;
  double wetCost = (double)10000000000000;
  mat2D<int>* spatialCover = coverStruct->spatial_arrays[0];

  clock_t t = clock();

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

  // Write the costs to a file
  int subsize = 7 + config->padsize;

  float* adk_LHwaveletImpact = new float[8*8*subsize*subsize];
  float* adk_HLwaveletImpact = new float[8*8*subsize*subsize];
  float* adk_HHwaveletImpact = new float[8*8*subsize*subsize];

  for (int modrow = 0; modrow < 8; modrow++) {
    for (int modcol = 0; modcol < 8; modcol++) {
      for (int rsub = 0; rsub < subsize; rsub++) {
        for (int csub = 0; csub < subsize; csub++) {
          adk_LHwaveletImpact[csub+rsub*subsize+modcol*subsize*subsize+modrow*subsize*subsize*8] =
              (float)LHwaveletImpact->Read(modrow, modcol)->Read(rsub, csub);
          adk_HLwaveletImpact[csub+rsub*subsize+modcol*subsize*subsize+modrow*subsize*subsize*8] =
              (float)HLwaveletImpact->Read(modrow, modcol)->Read(rsub, csub);
          adk_HHwaveletImpact[csub+rsub*subsize+modcol*subsize*subsize+modrow*subsize*subsize*8] =
              (float)HHwaveletImpact->Read(modrow, modcol)->Read(rsub, csub);
        }
      }
    }
  }

  float* adk_R_LH =
      new float[(coverStruct->image_height+32)*(coverStruct->image_width+32)];
  float* adk_R_HL =
      new float[(coverStruct->image_height+32)*(coverStruct->image_width+32)];
  float* adk_R_HH =
      new float[(coverStruct->image_height+32)*(coverStruct->image_width+32)];

  for (int row = 0; row < coverStruct->image_height + 32; row++) {
    for (int col = 0; col < coverStruct->image_width + 32; col++) {
      adk_R_LH[row * (coverStruct->image_width + 32) + col] =
          1.0 / (float)(R_LH->Read(row, col) + config->sigma);
      adk_R_HL[row * (coverStruct->image_width + 32) + col] =
          1.0 / (float)(R_HL->Read(row, col) + config->sigma);
      adk_R_HH[row * (coverStruct->image_width + 32) + col] =
          1.0 / (float)(R_HH->Read(row, col) + config->sigma);
    }
  }

  float* mycosts =
      new float[coverStruct->image_height * coverStruct->image_width];

  int idx1, idx1a, idx2, idx2a;

  for (int row = 0; row < (int)coverStruct->image_height; row++) {
    for (int col = 0; col < (int)coverStruct->image_width; col++) {
      int modRow = row % 8;
      int modCol = col % 8;

      int subRowsFrom = row - modRow - 6 + config->padsize;
      int subColsFrom = col - modCol - 6 + config->padsize;

      double rho = 0;

      for (int r_sub = 0; r_sub < 7 + config->padsize; r_sub++) {
        idx2a=(subRowsFrom+r_sub)*(coverStruct->image_width+32)+subColsFrom;
        idx1a=r_sub*subsize+modCol*subsize*subsize+modRow*subsize*subsize*8;

        for (int c_sub = 0; c_sub < 23; c_sub++) {
          idx1 = idx1a + c_sub;
          idx2 = idx2a + c_sub;
          rho += adk_LHwaveletImpact[idx1] * adk_R_LH[idx2];
          rho += adk_HLwaveletImpact[idx1] * adk_R_HL[idx2];
          rho += adk_HHwaveletImpact[idx1] * adk_R_HH[idx2];
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

  char* outfilename = new char[1024];
  sprintf(outfilename, "%s.juni.costs", filename);
  //printf("outfilename=%s\n", outfilename);
  FILE* outfile = fopen(outfilename, "wb");
  fwrite(mycosts, sizeof(float),
         coverStruct->image_height * coverStruct->image_width, outfile);

  /*
  for (int row=0; row < (int)coverStruct->image_height; row++) {
    for (int col=0; col < (int)coverStruct->image_width; col++) {
        float* pixel_costs = costs + ((col+row*cover->cols)*3);
        fprintf(outfile,"%.10f\n",pixel_costs[0]);
    }
  }
  */

  fclose(outfile);

  t = clock() - t;
  printf("%s\t%s\t%dx%d\tcost model took %.6fs\n",
         filename, outfilename,
         coverStruct->image_width, coverStruct->image_height,
         ((float)t) / CLOCKS_PER_SEC);
}

cost_model::~cost_model() {}
