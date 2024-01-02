#!/bin/bash


mkdir -p ./app/upload/fret/emission_files
mkdir -p ./app/upload/fret/extinction_coefficient_files
mkdir -p ./app/upload/fret/index_files
mkdir -p ./app/upload/fret/refractive_index_files
mkdir -p ./app/upload/fret/result
mkdir -p ./app/upload/ri/index_files
mkdir -p ./app/upload/ri/abs_coefficient_files
mkdir -p ./app/upload/ri/k_files
mkdir -p ./app/upload/ri/result
mkdir -p ./app/upload/plqsim/input_files
mkdir -p ./app/upload/plqsim/result
mkdir -p ./app/upload/tmmsim/input_files
mkdir -p ./app/upload/tmmsim/result

cp mocks/fret_calc_mock.py fret_calc.py
cp mocks/plq_sim_mock.py plq_sim.py
cp mocks/ri_calc_mock.py ri_calc.py
cp mocks/tmm_sim_mock.py tmm_sim.py
