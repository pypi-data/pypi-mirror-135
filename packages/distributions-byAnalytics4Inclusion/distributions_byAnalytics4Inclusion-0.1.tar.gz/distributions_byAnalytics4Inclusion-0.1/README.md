# distributions_byAnalytics4Inclusion
This package was created as part of Udacity's datascience curriculum.

It contains Gaussian and Binomial classes to easily compute and plot distributions.

#Files in Package
This package contains three files:

- Generaldistribution.py  : Creates the Distribution class defines the mean, stdev, and data attributes. And the read_data_file  method which populates the data attribute. Both the Gaussian and Binomial classes inheret the Distribution class.

- Gaussiandistribution.py: The Gaussian class contains methods specific to computing the mean, std, and plotting the pdf of a Guassian distribution. It also contains magic methods for 'add' and 'repr,' which combine Guassian distributions and will print out parameters of the combined distribution.

- Binomialdistribution.py: The Binomial class contains methods specific to computing the mean, std, and plotting the pdf of a Binomial distribution. It also contains magic methods for add and repr, which combine Binomial distributions and will print out parameters of the combined distribution.

#Installation

1. Simply pip install distibutions-byAnalytics4Inclusion
2. In your python interpreter: 
	- from distibutions-byAnalytics4Inclusion import Gaussian
    - from distibutions-byAnalytics4Inclusion import Binomial