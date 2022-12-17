import re # Module that searches for Regular Expressions (built-in)
import urllib.parse # Module that quotes URLs (pip install urllib)
from bs4 import BeautifulSoup # Module that processes HTML (pip install beautifulsoup4)

#######################################################################################################

'''
prettify replaces all Piazza markdowns in (text) with their corresponding Discord markdowns
Also replaces images with links, and LaTex with a link to the rendered image
Str -> Str
'''
def prettify(text, type):
    if type == 'content':
        # Removes formatting on empty line breaks #####################################################
        empty_lines = ['<strong></strong>', '<em></em>', '<code></code>', 
                       '<span style="text-decoration:underline"></span>', 
                       '<span style="text-decoration:line-through"></span>']
        for line in empty_lines:
            text = text.replace(line, '')
    
        # Piazza -> Discord markdown ##################################################################
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
        text = re.sub(pattern=r'<strong>(.+?)</strong>', repl=r'**\1**', string=text)
        # <em> italics </em>   ->   * italics *
        text = re.sub(pattern=r'<em>(.+?)</em>', repl=r'*\1*', string=text)
        # <code> code </code>   ->   ``` code ```
        text = re.sub(pattern=r'<code>(.+?)</code>', repl=r'```\1```', string=text)
        # <span style="text-decoration:underline"> underline </span>   ->   __ underline __
        text = re.sub(pattern=r'<span style="text-decoration:underline">(.+?)</span>', 
                         repl=r'__\1__', string=text)
        # <span style="text-decoration:line-through"> strikethrough </span>   ->   ~~ strikethrough ~~
        text = re.sub(pattern=r'<span style="text-decoration:line-through">(.+?)</span>', 
                         repl=r'~~\1~~', string=text)

        # Replaces HTML image tags with URL ###########################################################
        # <img src="{source}" />   ->   https://piazza.com{source}
        text = re.sub(r'<img src="(.+?)".+?/>', repl=' https://piazza.com'+r'\1 ', string=text)

        # Replaces LaTex with a link to the rendered image ############################################
        '''
        findall returns a list of all occurrences of (pattern) in (string)
        Str Str -> List of Str
        '''
        latex = re.findall(pattern='\$\$.+?\$\$', string=text)
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
            text = text.replace(line, 'https://latex.codecogs.com/png.image?%5Cdpi%7B300%7D%5Cbg%7Bblack%7D'+path)
            
        # >>> Discord quote markdown ###################################################################
        text = '>>> ' + text
    ####################################################################################################
    '''
    BeautifulSoup removes paragraph tags and translates HTML entities to Unicode characters
    Str Str -> Str
    '''
    text = BeautifulSoup(text, 'html.parser').text
    
    return text
