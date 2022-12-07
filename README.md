# Comic Scraper!

This silly little project was made to scrape certain comics from around the Interwebs.  
It was made out of boredome over the course of a weekend to try to learn a bit of web scraping.  
Python was chosen almost "just because" but partially because it had been a while since I had used Python and I read that it has decent libraries for web scraping.

## Getting This Running

To switch to the virtual environment:  
`source venv/bin/activate`

Update packages list:  
`python -m pip freeze > requirements.txt`

Install all packages:  
`python3 -m pip install -r requirements.txt`

Install new package:  
`python -m pip uninstall <package>`

Uninstall package:  
`python -m pip uninstall <package>`

To run  
`python3 run.py <options>`

- You HAVE to run it with one of the available options otherwise it will just yell at you.

TODO

Features to add

- ~~Logging system that shows which comic had an issue and which strip failed.~~
  - ~~Can use error handling to "gracefully skip over that failed one and go to the next while logging it to look into later.~~

Comics to add

- The Far Side (good luck with this one)
- Little Nemo (good luck finding all of them and in decent condition)
- Alley Oop (seems to never end and has been going for almost 100 years!)
- Buck Rogers?
- Flash gordon
- Prince Valiant
- Dick Tracy

[Go comics](https://www.gocomics.com) has a lot of comics up for free

Calvin and Hobbes ran from November 18, 1985 to December 31, 1995.
Dilbert started on August 16th, 1989 and is still going.
