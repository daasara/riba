# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ContactUs.phone'
        db.alter_column('feedback_contactus', 'phone', self.gf('django.db.models.fields.CharField')(max_length=10))


    def backwards(self, orm):
        
        # Changing field 'ContactUs.phone'
        db.alter_column('feedback_contactus', 'phone', self.gf('django.db.models.fields.CharField')(max_length=15))


    models = {
        'accounts.client': {
            'Meta': {'object_name': 'Client'},
            'clientdomain_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'confirmed_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> order@chaupaati.com'", 'max_length': '500'}),
            'confirmed_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'feedback_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> feedback@chaupaati.com'", 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_pricelist': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'noreply_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> noreply@chaupaati.com'", 'max_length': '200'}),
            'pending_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> lead@chaupaati.com'", 'max_length': '500'}),
            'pending_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'promotions_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> promotions@chaupaati.com'", 'max_length': '200'}),
            'sale_pricelist': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'share_product_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> share@chaupaati.com'", 'max_length': '500'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'sms_mask': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'feedback.contactus': {
            'Meta': {'object_name': 'ContactUs'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Client']", 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject': ('django.db.models.fields.CharField', [], {'default': "'general'", 'max_length': '50'}),
            'submitted_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 18, 16, 13, 58, 913758)'})
        },
        'feedback.customerimage': {
            'Meta': {'object_name': 'CustomerImage'},
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feedback.Feedback']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'feedback.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Client']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'submitted_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 18, 16, 13, 58, 912177)'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'feedback'", 'max_length': '25'})
        }
    }

    complete_apps = ['feedback']
