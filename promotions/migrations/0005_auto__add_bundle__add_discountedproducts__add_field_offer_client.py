# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bundle'
        db.create_table('promotions_bundle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('offer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotions.Offer'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=25)),
        ))
        db.send_create_signal('promotions', ['Bundle'])

        # Adding M2M table for field primary_products on 'Bundle'
        db.create_table('promotions_bundle_primary_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bundle', models.ForeignKey(orm['promotions.bundle'], null=False)),
            ('sellerratechart', models.ForeignKey(orm['catalog.sellerratechart'], null=False))
        ))
        db.create_unique('promotions_bundle_primary_products', ['bundle_id', 'sellerratechart_id'])

        # Adding model 'DiscountedProducts'
        db.create_table('promotions_discountedproducts', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bundle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['promotions.Bundle'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.SellerRateChart'])),
            ('percentage_off', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('promotions', ['DiscountedProducts'])

        # Adding field 'Offer.client'
        db.add_column('promotions_offer', 'client', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['accounts.Client']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Bundle'
        db.delete_table('promotions_bundle')

        # Removing M2M table for field primary_products on 'Bundle'
        db.delete_table('promotions_bundle_primary_products')

        # Deleting model 'DiscountedProducts'
        db.delete_table('promotions_discountedproducts')

        # Deleting field 'Offer.client'
        db.delete_column('promotions_offer', 'client_id')


    models = {
        'accounts.account': {
            'Meta': {'object_name': 'Account'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Client']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'confirmed_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> order@chaupaati.com'", 'max_length': '500'}),
            'confirmed_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'customer_support_no': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'dni': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'greeting_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'greeting_title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pending_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> lead@chaupaati.com'", 'max_length': '500'}),
            'pending_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'pg_return_url': ('django.db.models.fields.URLField', [], {'default': "'http://www.chaupaati.in'", 'max_length': '200', 'blank': 'True'}),
            'primary_email': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'primary_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'returns_policy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'secondary_email': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'secondary_phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'share_product_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> share@chaupaati.com'", 'max_length': '500'}),
            'shipping_policy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'sms_mask': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tos': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Channel'", 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'accounts.client': {
            'Meta': {'object_name': 'Client'},
            'confirmed_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> order@chaupaati.com'", 'max_length': '500'}),
            'confirmed_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pending_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> lead@chaupaati.com'", 'max_length': '500'}),
            'pending_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'share_product_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> share@chaupaati.com'", 'max_length': '500'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'sms_mask': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'catalog.availability': {
            'Meta': {'object_name': 'Availability'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'catalog.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'catalog.product': {
            'Meta': {'object_name': 'Product'},
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Brand']"}),
            'cart_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Category']"}),
            'confirmed_order_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'inr'", 'max_length': '3'}),
            'description': ('tinymce.models.HTMLField', [], {}),
            'ext_large_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ext_medium_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'ext_small_image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'has_images': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'moderate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pending_order_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '15', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '10'}),
            'video_embed': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'catalog.sellerratechart': {
            'Meta': {'object_name': 'SellerRateChart'},
            'availability': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Availability']"}),
            'cod_available_at': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cod_available_at'", 'null': 'True', 'to': "orm['catalog.Availability']"}),
            'cod_charge': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'condition': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '5', 'db_index': 'True'}),
            'external_product_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'external_product_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'gift_desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gift_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cod_available': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_prefered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'offer_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'payment_charges_paid_by': ('django.db.models.fields.CharField', [], {'default': "'chaupaati'", 'max_length': '15'}),
            'payment_collection_charges': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products_offered'", 'to': "orm['accounts.Account']"}),
            'shipping_charges': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'shipping_duration': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'shipping_paid_by': ('django.db.models.fields.CharField', [], {'default': "'vendor'", 'max_length': '15'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'stock_status': ('django.db.models.fields.CharField', [], {'default': "'instock'", 'max_length': '100'}),
            'transfer_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'visibility_status': ('django.db.models.fields.CharField', [], {'default': "'always_visible'", 'max_length': '100', 'db_index': 'True'}),
            'warranty': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'whats_in_the_box': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Client']"}),
            'ext_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'moderate': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Store']", 'null': 'True', 'blank': 'True'})
        },
        'categories.store': {
            'Meta': {'object_name': 'Store'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'promotions.bundle': {
            'Meta': {'object_name': 'Bundle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.Offer']"}),
            'primary_products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.SellerRateChart']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '25'})
        },
        'promotions.bundleoffer': {
            'Meta': {'object_name': 'BundleOffer'},
            'bundle_product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.SellerRateChart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.Offer']"}),
            'percentage_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '25'})
        },
        'promotions.coupon': {
            'Meta': {'unique_together': "(('code', 'status'),)", 'object_name': 'Coupon'},
            'applies_to': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'discount_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'discount_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'expires_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'given_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Account']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_uses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'inactive'", 'max_length': '25'}),
            'use_when': ('django.db.models.fields.CharField', [], {'default': "'manual'", 'max_length': '25'}),
            'uses': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'promotions.couponconstraint': {
            'Meta': {'object_name': 'CouponConstraint'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'account_coupons'", 'null': 'True', 'to': "orm['accounts.Account']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_coupons'", 'null': 'True', 'to': "orm['categories.Category']"}),
            'coupon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.Coupon']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logical_operator': ('django.db.models.fields.CharField', [], {'default': "'and'", 'max_length': "'3'"}),
            'order_min_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'product_qty_min': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['catalog.Product']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'promotions.discountedproducts': {
            'Meta': {'object_name': 'DiscountedProducts'},
            'bundle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.Bundle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_off': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.SellerRateChart']"})
        },
        'promotions.featuredproducts': {
            'Meta': {'object_name': 'FeaturedProducts'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Category']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']", 'null': 'True'}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Store']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'store'", 'max_length': '25', 'db_index': 'True'})
        },
        'promotions.offer': {
            'Meta': {'object_name': 'Offer'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ends_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price_label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'stackable': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '25'}),
            'starts_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '25'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'promotions.offerproduct': {
            'Meta': {'object_name': 'OfferProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['promotions.Offer']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.SellerRateChart']"}),
            'sticker_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'}),
            'transfer_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '2', 'blank': 'True'})
        }
    }

    complete_apps = ['promotions']
