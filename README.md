
## vogueX Fashion Recommender: Outfit Recommendation System
[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](https://github.com/SRN-SE-Fall24/FashionRecommender/blob/dev/README.md)
<a href =https://github.com/SRN-SE-Fall24/FashionRecommender/blob/dev/LICENCE.md><img src=https://img.shields.io/github/license/SRN-SE-Fall24/FashionRecommender></a>

[![Github Repo size in bytes](https://img.shields.io/github/languages/code-size/SRN-SE-Fall24/FashionRecommender)](https://github.com/SRN-SE-Fall24/FashionRecommender)
[![codecov](https://codecov.io/gh/SRN-SE-Fall24/FashionRecommender/branch/master/graph/badge.svg?token=PDVKSB4BAN)](https://codecov.io/gh/SRN-SE-Fall24/FashionRecommender)

[![DOI](https://zenodo.org/badge/890415506.svg)](https://doi.org/10.5281/zenodo.14211776)


[![GitHub issues](https://img.shields.io/github/issues/SRN-SE-Fall24/FashionRecommender)](https://github.com/SRN-SE-Fall24/FashionRecommender/issues?q=is%3Aopen)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/SRN-SE-Fall24/FashionRecommender)](https://github.com/SRN-SE-Fall24/FashionRecommender/issues?q=is%3Aissue+is%3Aclosed)
[![Github pull requests](https://img.shields.io/github/issues-pr/SRN-SE-Fall24/FashionRecommender)](https://github.com/SRN-SE-Fall24/FashionRecommender/pulls)
[![Github closed pull requests](https://img.shields.io/github/issues-pr-closed/SRN-SE-Fall24/FashionRecommender)](https://github.com/SRN-SE-Fall24/FashionRecommender/pulls?q=is%3Apr+is%3Aclosed)

[![github workflow](https://github.com/SRN-SE-Fall24/FashionRecommender/actions/workflows/style_checker.yml/badge.svg)](https://github.com/SRN-SE-Fall24/FashionRecommender/actions/workflows/style_checker.yml)
[![github workflow](https://github.com/SRN-SE-Fall24/FashionRecommender/actions/workflows/main.yml/badge.svg)](https://github.com/SRN-SE-Fall24/FashionRecommender/actions/workflows/main.yml)

![GitHub language count](https://img.shields.io/github/languages/count/SRN-SE-Fall24/FashionRecommender)
<!-- Start marker for language badge generation -->
![Python](https://img.shields.io/badge/Python-48.28%25-blue)
![HTML](https://img.shields.io/badge/HTML-38.26%25-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-6.75%25-blue)
![CSS](https://img.shields.io/badge/CSS-6.71%25-blue)
<!-- End marker for language badge generation -->


## ?Description</br>
Has it ever happened that you were all set with the perfect dress for your big day but you forgot to take a rain check? 

Well, don't worry. Our fashion recommender is here to save your day. This ain't any regular fashion recommender but a recommender that will look out for you not only in terms of style but in terms of comfort. Now you may think how would one do that? We do this by providing you choices based on:

  - Weather of the day, to let you know if you should avoid certain apparel or carry some extra accessories
  - Season to illustrate different patterns
  - Occasion to keep you in check with the highest rated choices 

There is feature of favourites where you can add your favourite attires to the favourites collection and can remove attires from the favourites.
We suggest Shopping links from e-commerce websites for the selected attires by distinguishing prices.

And if this doesn't seem enough, one can extend this in a thousand different ways, some of which are:

Integrating the health app with it to take an extra step and use the predicted menstrual cycle to enhance the outfit recommendation as to make it more comfortable.
Introducing a feedback mechanism to keep track of the user's preferences in order to give better suggestions
Integrating the calendar app to take care of the important days and send a recommendation accordingly.

We have 'A style for every story' so let it be known to the world :)

## Demo

[Click here to watch our demo!](https://drive.google.com/file/d/1q5wm0qu7Mw8gSYmC17TGPrOo3cX7KVop/view?usp=sharing) <br>


## ? Installation Procedure

## 1. Prerequisites 

Install the requirements using <br>
pip install -r requirements.txt <br><br>

In the project root folder,  <br>
Create a module: projectsecrets  <br>
ie. a folder named projectsecretes with a \_\_init\_\_.py inside it <br>

In this module, create files for secret variables <br>
1. For Gemini API <br>
   gemini_secret.py <br>
   GEMINI_API_KEY="YOUR_API_KEY" <br>
2. For Weather API <br>
   weather_secret.py <br>
   WEATHER_KEY="YOUR_API_KEY" <br>


## 2. Deploying

First, clone the repository:


$ git clone https://github.com/SRN-SE-Fall24/FashionRecommender


Change working directory to the repository:


$ cd Fashion-Recommender


We have made a python script to run the application.
Just run 

$ python3 main.py


### 3. Follow the provided address and enjoy!


http://localhost:5000/


## Contributors:
- Sharmeen Momin (smomin)
- Rutvik Kulkarni (rvkulkar)
- Nishad Tardalkar (ntardal)



## License
[MIT License](https://github.com/SRN-SE-Fall24/FashionRecommender/blob/master/LICENSE.md)

