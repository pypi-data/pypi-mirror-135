
# URL Obfuscator 
# Copyright (C) 2019-2022 M.Anish <aneesh25861@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
url=''

def void():
  

  #List of publicly discovered open_redirects.
  open_redirect=[ '--- URLS with Redirection Notice ---\n',

                'https://www.google.com/url?q=',  # Redirect using Google .[  Google Redirect Notice. ] [ source: Google ]
                'https://google.com/url?q='     , # Variant of above redirect. [ Warning prsent ] [ source: M.Anish ]
                'https://facebook.com/l.php?u=',  # Facebook Open Redirect       [ source : Google ]

                '\n--- URLS with No Redirection Warnings ---\n',

                'https://via.hypothes.is/' ,      # Annotation service.     [ No warning ] [ source : Google ]
                'http://vk.com/away.php?to=',     # Open Redirect in Russian Social Media vk.com [ No warning! ]
                'https://googleweblight.com/i?u=' ,# Redirect using Googleweblight [ No warning ]  [ source: Google ]
                'http://l.wl.co/l?u=',              # Open_redirect Whatsapp Business Account Profile website links. [ source:M.Anish]
                'https://proxy-02.onionsearchengine.com/index.php?q=', #Open_redirect in Proxy.[ No warning ][ source: M.Anish]
                'https://proxy-02.onionsearchengine.com/url.php?u=',  #Open_redirect.[ No warning ][ source: M.Anish ] 
                'http://raspe.id.au/bypass/miniProxy.php?', #Open_redirect in proxy [ No warning ] [ Difficult to detect ]
                'https://www.awin1.com/cread.php?awinmid=6798&awinaffid=673201&ued=', # [ No warning ]
                'https://www.anrdoezrs.net/click-6361382-15020510?url=', # [ No warning ]
                'https://www.digit.in/flipkart/intermediate?url=', # [ Easy to detect ]
                'https://adclick.g.doubleclick.net/pcs/click?xai=AKAOjstFA55hCSrFSTBDNko3225YAz6GkouTQlHjExWXRbT5OPMnSlE8Wh4LAVp-D7jWRr-LcKW0w-HH1g8lCVAK_eU-5azfUXfjqfTiHFOFWV9I8m2ZaGczGlov1iY8kMSnelCX-AHG6VYBmpcZJapT1XbdlOM3B9u9whYqpkxEpFLbkzwDao00-DL8JyS7UIxIApb_JHANRmtKLSuRcM8IWqFaP0cOc8n8jTedmwHc8oAw2MV2tRUaAnN3eaxaESpc8fovDeWslJ0A3duo5g46YzCYxQ8A56RI5MGcQw4TZj6TeWuj6jRjAe7g0X18--IBmztC1sUi6XuHkB1Ew-z_h9bv1XK-s_9L6zeDfQPtMsI3hOqp8T8545VdgCoElxs&sig=Cg0ArKJSzEpZ_YMvCKWCEAE&fbs_aeid=[gw_fbsaeid]&urlfix=1&adurl=', # [ No warning ]
                'https://shop-links.co/link?publisher_slug=future&exclusive=1&u1=tomsguide-in-2620345246174741000&url=', # [ No warning ]
                'https://googleads.g.doubleclick.net/dbm/clk?sa=L&ai=Ch1TErG3lYaXxE8GyvgTrwre4BvCz6uJn4uW17-wK8C4QASDfq6gIYOWCgIDYDqABsfr_6gLIAQmoAwGqBOkBT9B8PmcO1ZZkMxBDF7yrq7VVGoBuVw5N2Ylth__1CIqbJG66jQfYVl3bVTlKsTq1SbbnM7LX2-CECBg66suRCZt3avN24sTbMkdz6nCe9LqMJ23BLpBeKT1icbX7UWNOCgN-wCSCbVEEriRA5rNbaAwF5SQelEJKOKUolZhS2n9E6mtxappeRoygCWoKGclhg9klZDoe5XUDLhu68FvCDGlwHcZjBqc5u8Ke6wWFpRftfz3Gx9NLgteNqrpQ5rvz0vZnNIPiih0xpflpz37RoM7IzhaNhHq-Yxi3Zmma9XkCSXihr124NirABKnmh_y4AuAEA5AGAaAGTYAHt4WAlQGoB47OG6gHk9gbqAfulrECqAf-nrECqAfVyRuoB6a-G6gH89EbqAeW2BuoB6qbsQKoB9-fsQLYBwDSCAcIgGEQARgdgAoBmAsByAsBgAwBsBPn5PcN0BMA2BMNiBQB2BQB0BUBgBcB&ae=1&num=1&cid=CAASEuRo8Dw5F8O80VD2OFjI0mCg0A&sig=AOD64_0TXUUF1mkDEyyhy3Xk8NwWZqWK3w&client=ca-pub-9079061040234685&dbm_c=AKAmf-B3Ym2CRa2lGdA1Bo0vWyOsMZbRkYX-Ba_pmnVuyTJPxNDnGrhUeS9-Z6RWVCbMCfc3v5EA_espC75e9pCxvE9kr6yTUuO6fjT4qqxbFCyQdtFNINQbsiKFkb-J1ASNflV2yNzITYORgK0LxILW1s1EWeCrdg&cry=1&dbm_d=AKAmf-DGX41uB8nqF5ZUQmPNeU5LT0Nz_3s6Fg7aqpaSMTABnbtPgEj5n_E1C-EnJ_ODUDAtje7mAPkIrCjphZ5diWfiOlY_4gmzc8ufiWFjpYaOLmoVw3oi0i7bI5Ww6zbzKXIzBTF3GBm_weF9eDRMOQzAK07t3bx8ggWMZ0Yj6rV0kDt6i-9-XyriccB-e4bT5eriA__3zXEJjxmlXHJisAAMNeclGDnHxZPlNe2XDBaozLUGcXEVcBzSI0QTjRoyiLDqePhHiKHUBJA70nEqVSMZ1oHZss-mvAtVqEMumNWqhLpyG3lGT3askUav-0nDLdJjaLV8CzR5H0oQOACbs1dHyd8Y_c3ptCIn-sb2Nc9Y9w57tIvZzVt7jaZgTc9pVVjXpfe2eC4YA-HgjJ7ypbeIbwv-0fA8DYu36i-N3AANbdkL5HMJqnWhNT0bkmWV2QwmA5HN1fC4TDlXjH2k3sGV8hb8YEvDWYd3R2pwa4UrWvNLF1GmNWr5awFStF1jd3OOIvriU99pZ0N6ZF829wCKqTRWXyKDemFJfVQYngXdNowEXSY&adurl=', # [ No warning ]

                '\n--- ONION URLs ---\n',

                'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/redir.php?url=',#Redirect using Haystack DEEP WEB search. [ ONION SERVICE][source:M.Anish]
                'http://zgphrnyp45suenks3jcscwvc5zllyk3vz4izzw67puwlzabw4wvwufid.onion/url.php?u=', #Open_redirect  [ no warning . ]  

                '\n--- Tor Onion URL Redirection [ only works for sites ending with .onion ] ---\n',

                'https://ahmia.fi/search/search/redirect?search_term=cat&redirect_url=', #Redirect in Ahmia Search [ easily detectable]     
                'http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion/search/search/redirect?search_term=cat&redirect_url=' #Redirect Ahmia [ easily detectable]        
                            
                ]

  #Function to get URL from user which will be obfuscated by the program.                
  def get_url():
    print('\n Enter url: ',end='') 
    global url
    tmp=input()
    if tmp.startswith('http://') or tmp.startswith('https://'):
       url=tmp
    else:
       url='http://'+tmp

  get_url()

  #Function to write obfuscated URLs to url_obfuscated.txt file.
  def file_w():
    with open('url_obfuscated.txt','w') as f:
       for i in open_redirect:
          if '---' in i:
             f.write(i)
          else:
             f.write('{}{}\n'.format(i,url))
        
  file_w()

  #Function to obfuscate url using http basic auth.
  def http_basic_auth():
      custom_url=[
                 'https://accounts.google.com+signin=secure+v2+identifier=passive@',
                 'https://facebook.com+login=secure+settings=private@',
                 'https://instagram.com+accounts=login+settings=private@',
                 'https://linkedin.com+accounts=securelogin+settings=private@',
                 'https://github.com+login=secure+settings=private@'
                ]            
      with open('url_obfuscated.txt','a+')as f:
          f.write('\n--- Custom HTTP BASIC AUTH URLS [ Don\'t work in Firefox ] ---\n')
          for i in custom_url:
              if url.startswith('https://'):
                 f.write(i+url[8:]+'\n') 
              elif url.startswith('http://'):
                 f.write(i+url[7:]+'\n')

  http_basic_auth()            
  x=input( '\n {}/url_obfuscated.txt Generated!!!\n\nPress to continue...'.format(os.getcwd()))
