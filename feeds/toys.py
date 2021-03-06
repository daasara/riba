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
import simplejson

log = logging.getLogger('feeds')

class ToysFeed(Feed):
    config = {
            'ACCOUNT': 'my baby excel',
            }

    def get_model_name(self, sku):
        try:
            sku_info = SKUInfo.objects.get(account=self.config['ACCOUNT'],
                    sku=sku)
            if not sku_info.model:
                model = feedutils.get_letsbuy_model_number(sku)
                sku_info.model = model
                sku_info.save()
                return model
            else:
                return sku_info.model
        except SKUInfo.DoesNotExist:
            model = feedutils.get_letsbuy_model_number(sku)
            sku_info = SKUInfo(account=self.config['ACCOUNT'],
                    model=model,sku=sku)
            sku_info.save()
            return model
    
    def get_image_url(self,id):
        image_url = 'http://www.chaupaati.in/assets/images/adSnaps/' + id + '_thumb1.jpeg'
        return image_url


    def parse(self, sync, *args, **kwargs):

        #barbie url = 'http://192.168.91.101:8080/listing/select?indent=on&version=2.2&q=make%3Abarbie+AND+isActive%3Atrue&start=0&rows=100&fl=*%2Cscore&qt=standard&wt=json&explainOther=&hl.fl='

        #url = 'http://192.168.91.101:8080/listing/select?indent=on&version=2.2&q=make%3Adisney+AND+isActive%3Atrue&start=0&rows=100&fl=*%2Cscore&qt=standard&wt=json&explainOther=&hl.fl='

        #mattel url = 'http://192.168.91.101:8080/listing/select?indent=on&version=2.2&q=userId%3A208606+AND+isActive%3Atrue&start=0&rows=1000&fl=*%2Cscore&qt=standard&wt=json&explainOther=&hl.fl='

        url = 'http://192.168.91.101:8080/listing/select?indent=on&version=2.2&q=userId%3A209481+AND+isActive%3Atrue&start=0&rows=1000&fl=*&qt=standard&wt=json&explainOther=&hl.fl='

        json = urllib2.urlopen(url).read()
        dict = simplejson.loads(json)
        prods = dict['response']['docs']
        products = []
        for product in prods:
            if 'brand' not in product or not product['brand']:
                continue
            data = {'cleaned_data':self.get_default_cleaned_data()}
            # single value fields
            single_value_fields = ['id','sku','brand','description','mrp','askingPrice','title','shippingDuration']
            for field in single_value_fields:
                data[field] = ''
                if field in product:
                    data[field] = product[field]
            
            print '@@@',data
            # ignore blaclists
            #if self.is_blacklisted_brand(data['Brand_Name']): continue
            #if self.is_blacklisted_sku(data['SKU']): continue
            #if self.is_blacklisted_category(data['categories_name']): continue

            # create cleaned data 
            #data['cleaned_data']['brand_mapping'] = self.get_brand_mapping(data['Brand_Name'])
            #data['cleaned_data']['category_mapping'] = self.get_category_mapping(data['categories_name'])

            data['cleaned_data']['sku'] = data['sku']
            data['cleaned_data']['brand'] = Brand.objects.get(name=data['brand'])
            data['cleaned_data']['category'] = Category.objects.get(name='Toys & Games')
            data['cleaned_data']['model'] = data['sku']
            data['cleaned_data']['title'] = data['title']
            data['cleaned_data']['image_url'] = [self.get_image_url(data['id'])]
            data['cleaned_data']['shipping_duration'] = data['shippingDuration']
            data['cleaned_data']['offer_price'] = Decimal(str(data['askingPrice']).split('.')[0])            
            data['cleaned_data']['list_price'] = Decimal(str(data['mrp']).split('.')[0])
            data['cleaned_data']['description'] = striptags(data['description'])
            data['cleaned_data']['availability'] = AvailabilityMap.objects.get(
                    applies_to = 'account',
                    account = self.config['ACCOUNT']).availability
            products.append(data)

        return products


if __name__ == '__main__':
    feed = ToysFeed()
    feed.sync(**{'_local_':True})
