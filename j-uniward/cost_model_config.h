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

#ifndef CONFIG_H_
#define CONFIG_H_

#include "base_cost_model_config.h"
#include <vector>
#include "mat2D.h"

class cost_model_config : public base_cost_model_config
{
public:
	mat2D<double> * lpdf;
	mat2D<double> * hpdf;
	mat2D<double> * Tlpdf;
	mat2D<double> * Thpdf;
	mat2D<mat2D<double> *> * LHwaveletImpact;
	mat2D<mat2D<double> *> * HLwaveletImpact;
	mat2D<mat2D<double> *> * HHwaveletImpact;
	int padsize;
	double sigma;

	cost_model_config(float payload, bool verbose, int wavelet, unsigned int stc_constr_height, int randSeed);
	~cost_model_config();

private:
	void set_filters(int wavelet);
	void GetWaveletImpacts();
	double alpha(int coord);
};
#endif
