# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_parahraph = mars_news(browser)
    
    #for a web app it is not necessary to have headless as false (see the code in action)
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_parahraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemispheres()
    }

    #we want the automated browser to remain active while we are scraping data
    #then we should turn it down
    browser.quit()
    return data

# ### Pull article summaries and titles

# Visit the mars nasa news site
def mars_news(browser):
    
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text
        news_paragraph = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title,news_paragraph
# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ### Table of facts

def mars_facts():
    # Add try/except for error handling
    try:
        #It will take the first table it encounters
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #convert a data frame into html
    return df.to_html(classes="table table-striped")

def hemispheres():
    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # find the relative image url
    html = browser.html
    img_soup = soup(html,'html.parser')
    complete_links=[]
    for line in img_soup.find_all('a',class_="itemLink product-item"):
        h_img_url= f"https://marshemispheres.com/{line.get('href')}"
        if h_img_url not in complete_links:
            complete_links.append(h_img_url)
    complete_links.pop()

    hemisphere_image_urls = []
    for link in complete_links:
        browser.visit(link)
        im_html=browser.html
        he_img_soup = soup(im_html,'html.parser')
        he_title=he_img_soup.find('h2', class_='title').get_text()
        he_img_url_p=he_img_soup.find('a', target="_blank", string='Sample').get('href')
        he_img_url= f'https://marshemispheres.com/{he_img_url_p}'
        hemispheres={'img_url': he_img_url, 'title':he_title}
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    # 5. Quit the browser
    browser.quit()
    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls



#This tells flask that our script is complete and ready for action
if __name__ == "__main__":
    #If running as script, print scraped data
    #will print out the results of our scraping to our
    #terminal after executing the code
    print(scrape_all())