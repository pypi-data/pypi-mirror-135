# Signal Separation
## 0.0.8 version

Version 0.0.8 enables the simplest generation and separation of analytical chemistry signals consisting of two Gaussian peaks 100 wide, 0.8 to 15 high, difference from 0 to 100. The signal length is 1000 points.

The algorithm is based on theoretical considerations about the signal function contained in the paper (see reference 1).

## Features
- Genetic algorithm (see reference 2)
- Quick script for generating 1d-convolutional neural network architecture and training it (the possibility of setting the optimizer, grain, etc. in one line)
- Generation of a simple signal of two overlapping peaks with Gaussian distribution
- Modification of the cost function to compensate for the scarcity of the data (see: reference 3)
- **A script that estimates the positions and heights of peaks based on the generated signal (Uses CNN + SVR + Cost Modifications).**


## Installation


```sh
pip install signal-separation
```

## About ProjektInzynierski.ipynb and program.py

The ProjektInzynierski.ipynb file is an older, less polished, and safer version of the program. It can be run on the Google Colab platform. It uses the program.py file for its operation.

## License

*Free Software, 
made by Mieszko Pasierbek*

## References

[1] - J. Dubrovkin, „Mathematical methods for separation of overlapping asymmetrical peaks in spectroscopy and chromatography. Case study: one-dimensional signals”, International Journal of Emerging Technologies in Computational and Applied Sciences 11.1 (2015), 1–8.

[2] - T. Nagaoka, „Hyperparameter Optimization for Deep Learning-based Automatic Melanoma Diagnosis System”, Advanced Biomedical Engineering 9 (2020), 225

[3] - M. Steininger, K. Kobs, P. Davidson, A. Krause i A Hotho, „Density-based weighting for imbalanced regression”, Machine Learning 110 (2021), 2187–2211.