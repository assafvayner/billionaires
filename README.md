# Billionaires

This repository contains a website showing the vast wealth of America's top billionaires compared to the prices of different types of expensive items. It is largely inspired by "Spend Bill Gates' Money" which can be found [neal.fun/spend](neal.fun/spend).

This project is made using the plotly dash framework for web development with python. To run the website as is after cloning the repository run `app.py` recommendded python 3.7 and follow to the local host link to the website hosted on your machine. This will create some supplementary text files to keep track of when the website was last updated.

This project also uses the forbes400 api to retrieve data and their image api that do not require an api key. Measures are put in place so as not to call the api repeatedly unless needed. To ensure these measures are sustained to not delete the text files generated when running the website.