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

#include <vector>

#include "base_cost_model_config.h"
#include "cost_model_config.h"
#include "exception.hpp"
#include "mat2D.h"
#include "wavelets.h"

cost_model_config::cost_model_config(
  float payload, bool verbose, int waveletNumber,
  unsigned int stc_constr_height, int randSeed)
  : base_cost_model_config(payload, verbose, stc_constr_height, randSeed) {

	this->sigma = 0.0156;
	set_filters(waveletNumber);
	GetWaveletImpacts();
}

cost_model_config::~cost_model_config() {
	delete this->lpdf;
	delete this->Tlpdf;
	delete this->hpdf;
	delete this->Thpdf;

	delete LHwaveletImpact;
	delete HLwaveletImpact;
	delete HHwaveletImpact;
}

void cost_model_config::set_filters(int waveletNumber) {
	waveletEnum wavelet;

	switch (waveletNumber) {
		case 1:
      wavelet = daubechies8;
      break;
		default:
      throw exception("Unknown wavelet number.");
	}

	std::pair<mat2D<double>*, mat2D<double>*> filters =
      Wavelets::GetWavelets(wavelet);

	this->lpdf = filters.first;
	this->hpdf = filters.second;
	this->Tlpdf = mat2D<double>::Transpose(this->lpdf);
	this->Thpdf = mat2D<double>::Transpose(this->hpdf);

	if (this->lpdf->cols > this->hpdf->cols) {
    this->padsize = this->lpdf->cols;
  } else {
    this->padsize = this->hpdf->cols;
  }
}

double cost_model_config::alpha(int coord) {
	return coord == 0 ? sqrt(1.0/8) : sqrt(2.0/8);
}

void cost_model_config::GetWaveletImpacts() {
	// Spatial impact of an embedding change in DCT domain (with quantization 1)
	double PI = 3.14159265358979323846;
	mat2D<mat2D<double>*>* spatialImpact = new mat2D<mat2D<double>*>(8, 8);

  for (int u = 0; u < 8; u++) {
		for (int v = 0; v < 8; v++) {
			mat2D<double>* idctMat = new mat2D<double>(8, 8);

      for (int x = 0; x < 8; x++) {
				for (int y = 0; y < 8; y++) {
					idctMat->Write(x, y, alpha(u) * alpha(v) * cos((PI/8)*(x+0.5)*u) *
                         cos((PI/8)*(y+0.5)*v));
				}
			}

			spatialImpact->Write(u, v, idctMat);
		}
	}

	// Wavelet impact of an embedding change in DCT domain (with quantization 1)
	this->LHwaveletImpact = new mat2D<mat2D<double>*>(8, 8);
	this->HLwaveletImpact = new mat2D<mat2D<double>*>(8, 8);
	this->HHwaveletImpact = new mat2D<mat2D<double>*>(8, 8);

	for (int row = 0; row < 8; row++) {
		for (int col = 0; col < 8; col++) {
			LHwaveletImpact->Write(
        row, col,
        mat2D<double>::Correlation_Full_basicFilters(
          spatialImpact->Read(row, col), this->Tlpdf, this->hpdf));
			HLwaveletImpact->Write(
        row, col,
        mat2D<double>::Correlation_Full_basicFilters(
          spatialImpact->Read(row, col), this->Thpdf, this->lpdf));
			HHwaveletImpact->Write(
        row, col,
        mat2D<double>::Correlation_Full_basicFilters(
          spatialImpact->Read(row, col), this->Thpdf, this->hpdf));
		}
	}
}
