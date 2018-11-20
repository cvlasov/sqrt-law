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

#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include <time.h>
#include <vector>

#include <boost/filesystem.hpp>
#include <boost/program_options.hpp>

#include "cost_model.h"
#include "cost_model_config.h"
#include "exception.hpp"
#include "jstruct.h"

typedef unsigned int uint;
namespace fs = boost::filesystem;
namespace po = boost::program_options;

void printInfo() {
  std::cout << "This program provides a number of utilities related to JPEGs,"
            << "in particular related to J-UNIWARD embedding."
            << std::endl << std::endl;
  std::cout << "Author: Catherine Vlasov"
            << "Original author: Vojtech Holub, e-mail: vojtech_holub@yahoo.com"
            << std::endl << std::endl;
  std::cout << "usage: ./JPEG-UTILS [-v] -I input-dir [-z]"
            << std::endl << std::endl;
}

int main(int argc, char** argv) {
  try {
    std::string input_dir;
    bool verbose = false;
    bool print_nzAC = false;

    po::variables_map vm;
    std::vector<std::string> images;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help", "produce help message")
        ("input-dir,I",
         po::value<std::string>(&input_dir),
         "directory with images")
        ("images,i",
         po::value<std::vector<std::string> >(&images),
         "list of cover images")
        ("nzAC,z",
         po::bool_switch(&print_nzAC),
         "print the number of non-zero AC DCT coefficients in each image")
        ("verbose,v",
         po::bool_switch(&verbose),
         "print out verbose messages");

    po::positional_options_description p;

    po::store(
      po::command_line_parser(argc,argv).options(desc).positional(p).run(), vm);
    po::notify(vm);

    if (vm.count("help")) {
      printInfo();
      std::cout << desc << std::endl;
      return 1;
    }

    if (!vm.count("input-dir")) {
      std::cout << "'input-dir' is required." << std::endl << desc << std::endl;
      return 1;
    } else if (!fs::is_directory(fs::path(input_dir))) {
      std::cout << "'input-dir' must be an existing directory." << std::endl
                << desc << std::endl;
      return 1;
    }

    // Add all JPEG files from the input directory to the vector
    fs::directory_iterator end_itr;  // Default construction yields past-the-end

    if (vm.count("input-dir")) {
      for (fs::directory_iterator itr(input_dir); itr != end_itr; ++itr) {
        if ((!fs::is_directory(itr->status()))
            && (itr->path().extension() == ".jpg")) {
          images.push_back(itr->path().string());
        }
      }
    }

    int file_name_w = 16;
    int size_w = 11;
    int nzAC_w = 11;
    int time_w = 11;

    if (verbose) {
      std::cout << std::endl;
      std::cout << std::left << std::setw(file_name_w) << "File name"
                << std::left << std::setw(size_w) << "Size";

      if (print_nzAC) {
        std::cout << std::left << std::setw(nzAC_w) << "NzAC"
                  << std::left << std::setw(time_w) << "Time (s)";
      }

      std::cout << std::endl;
    }

    clock_t start = clock();

    cost_model_config* config = new cost_model_config(0.4, verbose, 1, 0, 0);
    float average_nzAC = 0.0;  // Approximate rolling average

    for (int imageIndex = 0; imageIndex < images.size(); imageIndex++) {
      fs::path imagePath(images[imageIndex]);
      jstruct* imageStruct = new jstruct(images[imageIndex], true);

      if (verbose) {
        std::stringstream stream;
        stream << imageStruct->image_height << "x" << imageStruct->image_width;
        std::string dimensions = stream.str();
        std::string file_name = imagePath.filename().string();
        std::cout << std::left << std::setw(file_name_w) << file_name
                  << std::left << std::setw(size_w) << dimensions
                  << std::flush;
      }

      clock_t image_start = clock();
      base_cost_model* model =
          (base_cost_model *)new cost_model(imageStruct, config);
      average_nzAC += model->nzAC / images.size();
      clock_t image_end = clock();

      if (verbose) {
        if (print_nzAC) {
          float seconds = \
              double(((double)image_end - image_start) / CLOCKS_PER_SEC);
          std::cout << std::left << std::setw(nzAC_w) << model->nzAC
                    << std::left << std::setw(time_w) << seconds;
        }

        std::cout << std::endl << std::flush;
      }

      delete imageStruct;
    }

    delete config;
    images.clear();

    clock_t end = clock();

    if (verbose) {
      std::cout << std::endl << "------------------------" << std::endl
                << "Average nzAC: " << int(average_nzAC) << std::endl
                << double(((double)end - start) / CLOCKS_PER_SEC)
                << " seconds elapsed" << std::endl;
    }

  } catch (std::exception& e) {
    std::cerr << "error: " << e.what() << std::endl;
    return 1;

  } catch (...) {
    std::cerr << "Exception of unknown type!" << std::endl;
  }
}
