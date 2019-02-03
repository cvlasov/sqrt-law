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
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/variate_generator.hpp>

#include "cost_model.h"
#include "cost_model_config.h"
#include "exception.hpp"
#include "jstruct.h"
#include "mat2D.h"
#include "mi_embedder.h"

typedef unsigned int uint;
namespace fs = boost::filesystem;
namespace po = boost::program_options;

void Save_Image(std::string imagePath, mat2D<int>* I);
mat2D<int>* Load_Image(std::string imagePath, cost_model_config* config);
mat2D<int>* Embed(float& alpha_out, float& distortion);

void printInfo() {
  std::cout << "This program embeds a payload using binary embedding while "
            << "minimizing 'J-UNIWARD' steganographic distortion to all "
            << "greyscale 'JPG' images in the directory input-dir and saves the"
            << "stego images into the output-dir." << std::endl << std::endl;
  std::cout << "Original author: Vojtech Holub, e-mail: vojtech_holub@yahoo.com"
            << std::endl << std::endl;
  std::cout << "Usage: BINARY-EMBEDDING -I input-dir -O output-dir "
            << "-b bits [-v]"
            << std::endl << std::endl;
}

int main(int argc, char** argv) {
  try {
    std::string iDir;
    std::string oDir;
    int payload_bits;
    bool verbose = false;
    int randSeed;

    po::variables_map vm;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("help,h", "produce help message")
        ("input-dir,I",
         po::value<std::string>(&iDir),
         "directory with the cover images")
        ("output-dir,O",
         po::value<std::string>(&oDir),
         "directory to output stego images")
        ("payload_bits,b",
         po::value<int>(&payload_bits),
         "payload to embed in bits")
        ("verbose,v",
         po::bool_switch(&verbose),
         "print out verbose messages")
        ("random-seed,r",
         po::value<int>(&randSeed)->default_value(0),
         "default=0 (every time different)");

    po::positional_options_description p;

    po::store(
      po::command_line_parser(argc,argv).options(desc).positional(p).run(), vm);
    po::notify(vm);

    if (vm.count("help")) {
      printInfo();
      std::cout << desc << std::endl;
      return 1;
    }

    if (!vm.count("output-dir")) {
      std::cout << "'output-dir' is required." << std::endl << desc
                << std::endl;
      return 1;
    } else if (!fs::is_directory(fs::path(oDir))) {
      std::cout << "'output-dir' must be an existing directory." << std::endl
                << desc << std::endl;
      return 1;
    }

    // Add all JPEG files (and corresponding cost files) from the input
    // directory to the vector of image/cost pairs
    std::vector<std::pair<std::string, std::string> > images;
    fs::directory_iterator end_itr;  // Default construction yields past-the-end
    fs::path output_dir(oDir);

    if (!vm.count("input-dir")) {
      std::cout << "'input-dir' is required." << std::endl << desc << std::endl;
      return 1;
    } else if (!fs::is_directory(fs::path(iDir))) {
      std::cout << "'input-dir' must be an existing directory." << std::endl
                << desc << std::endl;
      return 1;
    } else {
      for (fs::directory_iterator itr(iDir); itr != end_itr; ++itr) {
        if ((!fs::is_directory(itr->status()))
            && (itr->path().extension() == ".jpg")
            && (!fs::exists(oDir / itr->path().filename()))) {
          fs::path cost_file(itr->path());
          cost_file.replace_extension(".costs");
          images.push_back(std::make_pair(itr->path().string(),
                                          cost_file.string()));
        }
      }

      if (true) {
        std::cout << images.size() << " cover images to be embedded"
                  << std::endl;
      }
    }

    int file_name_w = 16;
    int seed_w = 6;
    int size_w = 11;
    int payload_w = 14;
    int distortion_w = 17;

    if (verbose) {
      std::cout << std::endl;
      std::cout << "J-UNIWARD DISTORTION EMBEDDING SIMULATOR" << std::endl;
      std::cout << "--> Input directory = " << iDir << std::endl;
      std::cout << "--> Output directory = " << oDir << std::endl;
      std::cout << "--> Running payload-limited sender with " << payload_bits
                << " bits" << std::endl;
      std::cout << "--> Simulating embedding as if the best coding scheme is "
                << "available" << std::endl;

      std::cout << std::endl;
      std::cout << std::left << std::setw(file_name_w)  << "File name"
                << std::left << std::setw(seed_w)       << "Seed"
                << std::left << std::setw(size_w)       << "Size"
                << std::left << std::setw(distortion_w) << "Rel. distortion"
                << std::endl << std::flush;
    }

    clock_t begin = clock();

    cost_model_config* config = new cost_model_config(
        payload_bits, verbose, 1, randSeed);

    for (int image_index = 0; image_index < (int)images.size(); image_index++) {
      fs::path cover_path(images[image_index].first);
      fs::path stego_path(
        fs::path(oDir) / fs::path(images[image_index].first).filename());

      // Load cover
      jstruct* cover_struct = new jstruct(images[image_index].first, true);

      if (cover_struct->coef_arrays.size() != 1) {
        throw new std::string("Error: Only grayscale images can be embedded.");
      }

      if (verbose) {
        std::stringstream stream;
        stream << cover_struct->image_height << "x"
               << cover_struct->image_width;
        std::string dimensions = stream.str();
        std::string file_name = cover_path.filename().string();
        std::cout << std::left << std::setw(file_name_w) << file_name
                  << std::left << std::setw(seed_w)      << randSeed
                  << std::left << std::setw(size_w)      << dimensions
                  << std::flush;
      }

      float* costs =
          new float[cover_struct->image_height * cover_struct->image_width];
      bool skip = false;

      // Read costs into float array
      std::ifstream cost_file(images[image_index].second.c_str());

      if (!cost_file) {
        std::cout << images[image_index].second << " doesn't exist. Skipping."
                  << std::endl;
        skip = true;
      }

      float cost;
      int count = 0;  // Used for error message
      int expected = cover_struct->image_height * cover_struct->image_width;

      for (int row = 0; row < cover_struct->image_height && !skip; row++) {
        for (int col = 0; col < cover_struct->image_width && !skip; col++) {
          if (cost_file >> cost) {
            count++;
            costs[col + row * cover_struct->image_width] = cost;
          } else {
            std::cout << "Not enough costs found (" << count << " out of "
                      << expected << " expected). Skipping." << std::endl;
            skip = true;
          }
        }
      }

      if (skip) {
        continue;  // Go to next image
      }

      // Embedding
      base_cost_model* model =
          (base_cost_model*)new cost_model(cover_struct, costs, config);

      if (false) {
        std::cout << std::endl << "Created cost model" << std::endl;
      }

      float distortion = 0;
      mat2D<int>* cover = cover_struct->coef_arrays[0];
      cover_struct->coef_arrays[0] = model->embed(distortion);

      if (false) {
        std::cout << "Finished embedding" << std::endl;
      }

      delete cover;
      delete model;

      // Save stego
      cover_struct->jpeg_write(stego_path.string(), true);

      if (verbose) {
        int pixels = cover_struct->image_height * cover_struct->image_width;
        int rel_distortion = distortion / pixels;
        std::cout << std::left << std::setw(distortion_w) << rel_distortion
                  << std::endl << std::flush;
      }

      if (false) {
        std::cout << "-----------" << std::endl << std::flush;
      }

      delete cover_struct;
    }

    delete config;
    images.clear();

    clock_t end = clock();

    if (verbose) {
      std::cout << "------------------------" << std::endl
                << std::endl << "Time elapsed: "
                << double(((double)end - begin) / CLOCKS_PER_SEC) << "s"
                << std::endl << std::endl;
    }

  } catch (std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
    return 1;

  } catch (...) {
    std::cerr << "Exception of unknown type!" << std::endl;
  }
}
