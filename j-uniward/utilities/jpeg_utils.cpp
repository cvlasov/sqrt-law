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

#include "exception.hpp"
#include "jstruct.h"

typedef unsigned int uint;
namespace fs = boost::filesystem;
namespace po = boost::program_options;

void printInfo() {
  std::cout << "This program provides a number of JPEG utilities, "
            << "in particular related to J-UNIWARD embedding."
            << std::endl << std::endl;
  std::cout << "Author: Catherine Vlasov" << std::endl
            << "J-UNIWARD author: Vojtech Holub (vojtech_holub@yahoo.com)"
            << std::endl << std::endl;
  std::cout << "Usage: ./JPEG-UTILS -C cover-dir -S stego-dir [-z] [-d]"
            << std::endl << std::endl;
}

int checkDirArg(std::string arg_name, std::string arg_val,
                std::string reason, po::variables_map vm) {
  if (!vm.count(arg_name)) {
    std::cout << "'" << arg_name << "' is required to " << reason << "."
              << std::endl;
    return 1;
  } else if (!fs::is_directory(fs::path(arg_val))) {
    std::cout << "'" << arg_name << "' must be an existing directory."
              << std::endl;
    return 1;
  }

  return 0;
}

void fillImageVector(std::string dir_name, std::vector<std::string>* images) {
  fs::directory_iterator end_itr;  // Default construction yields past-the-end

  for (fs::directory_iterator itr(dir_name); itr != end_itr; ++itr) {
    if ((!fs::is_directory(itr->status()))
        && (itr->path().extension() == ".jpg")) {
      images->push_back(itr->path().string());
    }
  }
}

int countDifferentCoefficients(jstruct* cover_struct, jstruct* stego_struct) {
  int diff_count = 0;
  for (int row = 0; row < cover_struct->image_height; row++) {
    for (int col = 0; col < cover_struct->image_width; col++) {
      if (!((row % 8 == 0) && (col % 8 == 0))
          && (cover_struct->coef_arrays[0]->Read(row, col)
              != stego_struct->coef_arrays[0]->Read(row,col))) {
        diff_count++;
      }
    }
  }
  return diff_count;
}

int countNzAC(jstruct* cover_struct) {
  int nzAC_count = 0;
  for (int row = 0; row < cover_struct->image_height; row++) {
    for (int col = 0; col < cover_struct->image_width; col++) {
      if (!((row % 8 == 0) && (col % 8 == 0))
          && (cover_struct->coef_arrays[0]->Read(row, col) != 0)) {
        nzAC_count++;
      }
    }
  }
  return nzAC_count;
}

int main(int argc, char** argv) {
  try {
    std::string cover_dir;
    std::string stego_dir;
    bool compare_cover_stego = false;
    bool print_nzAC = false;

    po::variables_map vm;
    std::vector<std::string> cover_images;
    std::vector<std::string> stego_images;

    po::options_description desc("Allowed options");
    desc.add_options()
        ("cover-dir,C",
         po::value<std::string>(&cover_dir),
         "directory with cover images")
        ("cover-images,c",
         po::value<std::vector<std::string> >(&cover_images),
         "list of cover images")
        ("diff-coef,d",
         po::bool_switch(&compare_cover_stego),
         "print the number of AC DCT coefficients that differ in each cover/"
         "stego image pair")
        ("help,h", "produce help message")
        ("stego-dir,S",
         po::value<std::string>(&stego_dir),
         "directory with stego images")
        ("stego-images,s",
         po::value<std::vector<std::string> >(&stego_images),
         "list of stego images")
        ("nzAC,z",
         po::bool_switch(&print_nzAC),
         "print the number of non-zero AC DCT coefficients in each cover "
         "image");

    po::positional_options_description p;

    po::store(
      po::command_line_parser(argc,argv).options(desc).positional(p).run(), vm);
    po::notify(vm);

    if (vm.count("help")) {
      printInfo();
      std::cout << desc << std::endl;
      return 1;
    }

    if (checkDirArg("cover-dir", cover_dir, "run JPEG-UTILS", vm) > 0
        || checkDirArg("stego-dir", stego_dir, "run JPEG-UTILS", vm) > 0) {
      return 1;
    }

    fillImageVector(cover_dir, &cover_images);
    fillImageVector(stego_dir, &stego_images);

    if (cover_images.size() != stego_images.size()) {
      std::cout << "Different number of cover images (" << cover_images.size()
                << ") and stego images (" << stego_images.size() << ")!"
                << std::endl;
      return 1;
    }

    int file_name_w = 16;
    int size_w = 11;
    int nzAC_w = 11;
    int diff_coef_w = 11;
    int time_w = 11;

    std::cout << std::endl;
    std::cout << std::left << std::setw(file_name_w) << "File name"
              << std::left << std::setw(size_w) << "Size";

    if (print_nzAC) {
      std::cout << std::left << std::setw(nzAC_w) << "NzAC";
    }

    if (compare_cover_stego) {
      std::cout << std::left << std::setw(diff_coef_w) << "Diff coef";
    }

    std::cout << std::left << std::setw(time_w) << "Time (s)" << std::endl;

    clock_t start = clock();
    float average_nzAC = 0.0;
    float average_diff_coef = 0.0;

    for (int imageIndex = 0; imageIndex < cover_images.size(); imageIndex++) {
      clock_t image_start = clock();
      fs::path cover_path(cover_images[imageIndex]);
      jstruct* cover_struct = new jstruct(cover_images[imageIndex], true);

      std::stringstream stream;
      stream << cover_struct->image_height << "x"
             << cover_struct->image_width;
      std::string dimensions = stream.str();
      std::string file_name = cover_path.filename().string();
      std::cout << std::left << std::setw(file_name_w) << file_name
                << std::left << std::setw(size_w) << dimensions
                << std::flush;

      if (print_nzAC) {
        int nzAC_count = countNzAC(cover_struct);
        average_nzAC += nzAC_count / cover_images.size();
        std::cout << std::left << std::setw(nzAC_w) << nzAC_count;
      }

      if (compare_cover_stego) {
        jstruct* stego_struct = new jstruct(stego_images[imageIndex], true);
        int diff_coef = countDifferentCoefficients(cover_struct, stego_struct);
        std::cout << std::left << std::setw(diff_coef_w) << diff_coef;
        average_diff_coef += diff_coef / cover_images.size();
        delete stego_struct;
      }

      delete cover_struct;
      clock_t image_end = clock();

      float seconds =
          double(((double)image_end - image_start) / CLOCKS_PER_SEC);
      std::cout << std::left << std::setw(time_w) << seconds
                << std::endl << std::flush;
    }

    cover_images.clear();
    stego_images.clear();
    clock_t end = clock();

    std::cout << std::endl << "------------------------" << std::endl;

    if (print_nzAC) {
      std::cout << "Average nzAC: " << int(average_nzAC) << std::endl;
    }

    if (compare_cover_stego) {
      std::cout << "Average # of different coefficients: "
                << int(average_diff_coef) << std::endl;
    }

    std::cout << "------------------------" << std::endl
              << double(((double)end - start) / CLOCKS_PER_SEC)
              << " seconds elapsed" << std::endl << std::endl;

  } catch (std::exception& e) {
    std::cerr << "error: " << e.what() << std::endl;
    return 1;

  } catch (...) {
    std::cerr << "Exception of unknown type!" << std::endl;
  }
}
