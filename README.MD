authors: shriya shah, dana chen, chloe chen, vincy cai
this program analyzes an image of a flying object and tells you if its a bird, plane, or neither! 

process:
take image
use gemini to make sure not random thing, either bird or plane
scan for plane data
if planes nearby, ask gemini to see which plane, then print plane information
if no planes/image doesnt match, send to bird classifier
bird classifier checks, prints bird info + facts from gemini
this program analyzes an image of a flying object and tells you if its a bird, plane, or neither!

.env.example --- Input your own keys!
    OPENSKY_CLIENT_ID & OPENSKY_CLIENT_SECRET: https://opensky-network.org/my-opensky/account 
        Create an account by following the link and generate your id and secret
