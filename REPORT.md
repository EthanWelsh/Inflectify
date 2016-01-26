#For each of the specified types, what are some variations that your program can cover?
My program can handle all of the specified types:
61              --> Sixty One
1,234           --> One Thousand Two Hundred Thirty Four
6.34            --> Six Point Three Four
3rd             --> Third
2 1\/2          --> Two and One Half
7 %             --> Seven Percent
7 3\/4 %        --> Seven and Three Fourths Percent
1:30 p.m        --> One Thirty p.m
$ 3.24          --> Three Dollars and Twenty Four Cents
$ 14.2 million  --> Fourteen Point Two million Dollars 
$7 3\/4 Million --> Seven and Three Fourths Million Dollar
2010            --> Twenty Ten
2001            --> Two Thousand and One
1900            --> Nineteen hundred
1903            --> Nineteen oh Three
1910s           --> Nineteen Tens
1980s           --> Nineteen Eighties 
January 1 2016  --> January First, Twenty Sixteen
May 19 2012     --> May Nineteenth, Twenty Twelve    
jan. 1st        --> january first
December 2016   --> December Twenty Sixteen
the 1st of 2016 --> the first of Twenty Sixteen
1/1/2016        --> January First, Twenty Sixteen
1/1/16          --> January First, Twenty Sixteen
1/1/93          --> January First, Nineteen Ninety Three
mid-1992        --> mid Nineteen Ninety Two
19-month        --> Nineteen month
Mr. Guy         --> mister guy
Mrs. Girl       --> miss girl
Dr. Dude        --> doctor dude
U.S             --> United States
Me vs. You      --> me verse you
5:3             --> Five to Three
5'23"           --> Five feet and Twenty Three inches 
5'1"            --> Five feet and One inch
XIV             --> Fourteen
MMXVI           --> Two Thousand Sixteen


#What was your strategy for identifying variations, given that you probably don’t want to read every sentence? 
In order to best be able to cover all of the numerous cases, I designed my code such that it worked in layers. Each line of input is passed through multiple functions which check for the presence of certain cases (e.g. dates, money, numbers), and then provide the correct English equivalent. Each layer or filter of my algorithm builds off of the previous one, such that it can gracefully handle combinations of cases, even those that haven't yet been seen.  

#Were there difficult cases that your program cannot correctly handle using regular expression matching?  If so, what additional tools do you think might be needed? 
There were a few cases that I found where my algorithm did not adept itself easily to solving them. These cases would not be hard to implement per say, but in order to avoid bloating my logic I tended away from fixing every little idiosyncrasy I could find. In order to more effectively capture all the edge cases without bloating logic, it would probably become necessary to employ some degree of machine learning to capture the more complex patterns of the English language. 

$ 18-to-$19                  --> Eighteen Dollars to Nineteen Dollars       (Eighteen to Nineteen Dollars)
a $ 1 billion cereal plant   --> a One billion Dollars cereal plant         (a One billion Dollar cereal plant)        
