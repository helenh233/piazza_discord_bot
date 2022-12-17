import re # Module that searches for Regular Expressions (built-in)
import urllib.parse # Module that quotes URLs ()
from bs4 import BeautifulSoup # (pip install beautifulsoup4)

###############################################################################################

'''
prettify replaces all Piazza markdowns in (content) with their corresponding Discord markdowns
Also replaces images with links, and LaTex with a link to the rendered image
Str -> Str
'''
def prettify(content):

    # Removes formatting on empty line breaks ##################################################
    empty_lines = ['<strong></strong>', '<em></em>', '<code></code>', 
                   '<span style="text-decoration:underline"></span>', 
                   '<span style="text-decoration:line-through"></span>']
    for line in empty_lines:
        content = content.replace(line, '')
    
    # Piazza -> Discord markdown ##############################################################
    '''
    re.sub returns (string) with all instances of (pattern) replaced with (repl)
    Str Str Str -> Str
    Regular expressions used in the raw string (pattern):
        '.+' matches a non-zero substring containing any characters (except '\n')
        '?' matches as few characters as possible
    Regular expressions used in the raw string (repl):
        '\1' will be replaced with the matched substring enclosed by '()' in (pattern)
    '''    
    # <strong> bold </strong>   ->   ** bold **
    content = re.sub(pattern=r'<strong>(.+?)</strong>', repl=r'**\1**', string=content)
    # <em> italics </em>   ->   * italics *
    content = re.sub(pattern=r'<em>(.+?)</em>', repl=r'*\1*', string=content)
    # <code> code </code>   ->   ``` code ```
    content = re.sub(pattern=r'<code>(.+?)</code>', repl=r'```\1```', string=content)
    # <span style="text-decoration:underline"> underline </span>   ->   __ underline __
    content = re.sub(pattern=r'<span style="text-decoration:underline">(.+?)</span>', 
                     repl=r'__\1__', string=content)
    # <span style="text-decoration:line-through"> strikethrough </span>   ->   ~~ strikethrough ~~
    content = re.sub(pattern=r'<span style="text-decoration:line-through">(.+?)</span>', 
                     repl=r'~~\1~~', string=content)

    # Replaces HTML image tags with URL ###########################################################
    # <img src="{source}" />   ->   https://piazza.com{source}
    content = re.sub(r'<img src="(.+?)".+?/>', repl=' https://piazza.com'+r'\1 ', string=content)

    # Replaces LaTex with a link to the rendered image ############################################
    '''
    findall returns a list of all occurrences of (pattern) in (string)
    Str Str -> List of Str
    '''
    latex = re.findall(pattern='\$\$.+?\$\$', string=content)
    for line in latex:
        '''
        string.strip(chars) returns (string) with the leading and trailing (chars) removed
        Str -> Str
        '''
        tex = line.strip('$')
        '''
        urllib.parse.quote(string) replaces special characters in (string) using the %xx escape
        Used to encode the path section of a URL
        Str -> Str
        '''
        path = urllib.parse.quote(tex)
        content = content.replace(line, 'https://latex.codecogs.com/png.image?%5Cdpi%7B300%7D%5Cbg%7Bblack%7D'+path)

    # >>> Discord quote markdown
    content = '>>> ' + BeautifulSoup(content, 'html.parser').text
    
    return content
