import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tinla.settings'

ROOT_FOLDER = os.path.realpath(os.path.dirname(__file__))
ROOT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')]

if ROOT_FOLDER not in sys.path:
    sys.path.insert(1, ROOT_FOLDER + '/')

# also add the parent folder
PARENT_FOLDER = ROOT_FOLDER[:ROOT_FOLDER.rindex('/')+1]
if PARENT_FOLDER not in sys.path:
    sys.path.insert(1, PARENT_FOLDER)

import urllib2
import urllib
from lxml import etree
from categories.models import Category
from catalog.models import Brand, Product, SellerRateChart, Availability
from utils import htmlutils
from feeds.models import *
from feeds import feedutils
from feeds.feed import Feed
from django.template.defaultfilters import slugify, striptags
import logging
from django.conf import settings
from decimal import Decimal
from django.utils.html import strip_tags
from BeautifulSoup import BeautifulSoup
import os

log = logging.getLogger('feeds')

class FutureBazaarFeed(Feed):
    config = {
            'ACCOUNT': 'futurebazaar',
            'URL': {
                'electronic-deals':'http://futurebazaar.com/atom?name=FutureBazaar&cat=Electronic+Deals',
                'home-deals':'http://futurebazaar.com/atom?name=FutureBazaar&cat=Home+Deals',
                'fashion-deals':'http://futurebazaar.com/atom?name=FutureBazaar&cat=Fashion+Deals'
                },
            'TYPE': 'XML'
            }

    def clean(self,string):
        keys = [u'\xef',u'\xa0',u'\xa1',u'\xa2',u'\xa3',u'\xa4',u'\xa5',u'\xa6',u'\xa7',u'\xa8',u'\xa9',u'\xaa',u'\xab',u'\xac',u'\xad',u'\xae',u'\xaf',u'\xb0',u'\xb1',u'\xb2',u'\xb3',u'\xb4',u'\xb5',u'\xb6',u'\xb7',u'\xb8',u'\xb9',u'\xba',u'\xbb',u'\xbc',u'\xbd',u'\xbe',u'\xbf',u'\xef',u'\xeb',u'\xf6',u'\xd7',u'\xe9']
        for key in keys:
            string = string.replace(key,u'')

        if not string:
            return ''
        string = str(string)
        string = string.strip()
        return string.replace('\\t','')
 
    def get_brand_for_futurebazaar(self, sku, url):
        try:
            sku_info = SKUInfo.objects.get(account=self.config['ACCOUNT'],
                    sku=sku)
            if sku_info.brand.name == "Unknown"  or not sku_info.brand:
                brand = feedutils.get_brand_for_futurebazaar(url)
                brand_mapping  = self.get_brand_mapping(brand).mapped_to
                sku_info.brand = brand_mapping
                sku_info.save()
                return brand_mapping
            else:
                return sku_info.brand
        except SKUInfo.DoesNotExist:
            brand = feedutils.get_brand_for_futurebazaar(url)
            brand_mapping  = self.get_brand_mapping(brand).mapped_to
            sku_info = SKUInfo(account=self.config['ACCOUNT'], sku=sku, brand = brand_mapping)
            sku_info.save()
            return brand_mapping

    def parse(self, sync, *args, **kwargs):
        # create the directory to store data
        os.mkdir('%s/%s-%s' % (settings.FEEDS_ROOT, self.config['ACCOUNT'], sync.id))
        files = []
        for url_name in self.config['URL'].keys():
            url = self.config['URL'][url_name]
            # get the file and save it
            path = '%s/%s-%d/%s.%s' % (settings.FEEDS_ROOT,
                    self.config['ACCOUNT'],
                    sync.id,
                    url_name,
                    self.config['TYPE'].lower())
            #class MyURLopener(urllib.FancyURLopener):
            #    def http_error_default(self, url, fp, errorcode, errmsg, headers):
            #        raise Exception("Unable to fetch file")
            #MyURLopener().retrieve(url, path)
            os.system("touch %s" % path)
            os.system("wget -t 10 -O '%s' '%s'" % (path,url))
            files.append(path)
            #files.append('%s/%s-%d/%s.%s' % (settings.FEEDS_ROOT,
            #    self.config['ACCOUNT'],
            #    sync.id,
            #    url_name,
            #    self.config['TYPE'].lower()))

        products = []
        for file in files:
            try:
                xmldoc = etree.parse(file)
                entries = xmldoc.xpath('/n:feed/n:entry', namespaces =
                        {
                            'n':'http://purl.org/atom/ns#',
                            'fb':'http://localhost:8080/atom', 
                            'dc':'http://purl.org/dc/elements/1.1/'
                        })
            except:
                entires = []
            for product in entries:
                data = dict(cleaned_data=self.get_default_cleaned_data())
                fields = {'sku': 'fb:skuid', 'product_name':'fb:productname', 'product_id': 'fb:productid','product_link':'fb:productlink',
                        'list_price':'fb:mrp', 'offer_price':'fb:saleprice',
                        'desc':'fb:productdesc', 'image':'fb:imagelink',
                        'category': 'fb:subcategory', 'url':'fb:productlink',
                        'subcategory': 'fb:subsubcategory', 'subsubcategory': 'fb:subsubsubcategory'}

                extracted_data = {}
                for key in fields:
                    node = product.xpath(fields[key], namespaces =
                            {
                                'n':'http://purl.org/atom/ns#',
                                'fb':'http://localhost:8080/atom', 
                                'dc':'http://purl.org/dc/elements/1.1/'
                            }) 
                    if node and len(node) > 0 and node[0].text:
                        extracted_data[key] = self.clean(node[0].text)
                    else:
                        extracted_data[key] = None


                cat = extracted_data['category']
                if extracted_data.get('subcategory', None):
                    cat = extracted_data['subcategory']
                if extracted_data.get('subsubsubcategory',None):
                    cat = extracted_data['subsubsubcategory']

                print extracted_data['url']

                extracted_data['brand'] = self.get_brand_for_futurebazaar(
                        extracted_data['sku'],
                        extracted_data['url'])

                print cat, extracted_data['brand']


                # ignore blaclists
                if self.is_blacklisted_sku(extracted_data['sku']): continue
                # create cleaned data 
                data['cleaned_data']['brand'] = self.get_brand_mapping(extracted_data['brand']).mapped_to
                data['cleaned_data']['category'] = self.get_category_mapping(cat).mapped_to

                data['cleaned_data']['sku'] = extracted_data['sku']
                data['cleaned_data']['external_product_id'] = extracted_data['product_id']
                data['cleaned_data']['external_product_link'] = extracted_data['product_link']
                data['cleaned_data']['model'] = ''
                data['cleaned_data']['title'] = extracted_data['product_name']
                data['cleaned_data']['image_url'] = [extracted_data['image']]
                #data['cleaned_data']['shipping_duration'] = '7-10 Working Days'
                data['cleaned_data']['list_price'] = Decimal(extracted_data['list_price'])
                
                data['cleaned_data']['offer_price'] = Decimal(extracted_data['offer_price'])
                if not extracted_data['list_price'] or extracted_data['list_price'] < extracted_data['offer_price']:
                    data['cleaned_data']['list_price'] = extracted_data['offer_price']
                data['cleaned_data']['description'] = extracted_data['desc'] or ''
                data['cleaned_data']['availability'] = AvailabilityMap.objects.get(
                        applies_to = 'account',
                        account = self.config['ACCOUNT']).availability
                products.append(data)

        #return []
        return products


if __name__ == '__main__':
    feed = FutureBazaarFeed()
    feed.sync()
