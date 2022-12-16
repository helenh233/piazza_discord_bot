import re # Regular Expression module
import urllib.parse
from bs4 import BeautifulSoup

#################################################

# prettify changes all Piazza markdown conventions in (content) to Discord.
# replaces images and latex with links to their source
# Str -> Str
def prettify(content):

    # Remove formatting on empty line breaks
    content = content.replace('<strong></strong>', '')
    content = content.replace('<em></em>', '')

    # re.sub finds all instances of (pattern) in (string) and replaces it with (repl)
    # Str Str Str -> Str
    # Regular expressions used:
        # . matches any character (except '\n')
        # +? minimal quantifier (matches as few characters as possible)
        #(causes the resulting Regular Expression to match 1+ repetitions of the preceding Regular Expression)

    # Piazza -> Discord markdown
    # <strong> bold </strong>   ->  ** bold **
    content = re.sub(pattern=r'<strong>(.+?)</strong>', repl=r'**\1**', string=content)
    # <em> italics </em>    ->  * italics *
    content = re.sub(pattern=r'<em>(.+?)</em>', repl=r'*\1*', string=content)
    # <code> code </code>   ->  ``` code ```
    content = re.sub(pattern=r'<code>(.+?)</code>', repl=r'```\1```', string=content)
    # <span style="text-decoration:underline"> underline </span>    ->  __ underline __
    content = re.sub(pattern=r'<span style="text-decoration:underline">(.+?)</span>', repl=r'__\1__', string=content)
    # <span style="text-decoration:line-through"> strikethrough </span>     ->  ~~ strikethrough ~~
    content = re.sub(pattern=r'<span style="text-decoration:line-through">(.+?)</span>', repl=r'~~\1~~', string=content)

    # Replace HTML image tags: <img src="____" /> with URL: https://piazza.com____
    content = re.sub(r'<img src="(.+?)".+?/>', repl=' https://piazza.com'+r'\1 ', string=content)

    # findall returns a list of all occurrences that match a given (pattern) in (string)
    # Str Str -> List of Str
    latex = re.findall(pattern='\$\$.+?\$\$', string=content)
    for line in latex:
        # Remove '$$' from beginning and end
        # Str -> Str
        tex = line.strip('$')
        # Encode URLs
        tex = urllib.parse.quote(tex)
        # Replace with URL to image of compiled LaTex
        content = content.replace(line, 'https://latex.codecogs.com/png.image?%5Cdpi%7B300%7D%5Cbg%7Bblack%7D'+tex)

    # >>> Discord quote
    content = '>>> ' + BeautifulSoup(content, 'html.parser').text
    return content
