# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Feedback.type'
        db.add_column('feedback_feedback', 'type', self.gf('django.db.models.fields.CharField')(default='feedback', max_length=25), keep_default=False)

        # Changing field 'Feedback.email'
        db.alter_column('feedback_feedback', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True))

        # Changing field 'Feedback.phone'
        db.alter_column('feedback_feedback', 'phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True))

        # Changing field 'Feedback.name'
        db.alter_column('feedback_feedback', 'name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True))


    def backwards(self, orm):
        
        # Deleting field 'Feedback.type'
        db.delete_column('feedback_feedback', 'type')

        # Changing field 'Feedback.email'
        db.alter_column('feedback_feedback', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Changing field 'Feedback.phone'
        db.alter_column('feedback_feedback', 'phone', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'Feedback.name'
        db.alter_column('feedback_feedback', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))


    models = {
        'accounts.client': {
            'Meta': {'object_name': 'Client'},
            'confirmed_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> order@chaupaati.com'", 'max_length': '500'}),
            'confirmed_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'noreply_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> noreply@chaupaati.com'", 'max_length': '200'}),
            'pending_order_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> lead@chaupaati.com'", 'max_length': '500'}),
            'pending_order_helpline': ('django.db.models.fields.CharField', [], {'default': "'0-922-222-1947'", 'max_length': '25'}),
            'share_product_email': ('django.db.models.fields.CharField', [], {'default': "'<Chaupaati Bazaar> share@chaupaati.com'", 'max_length': '500'}),
            'signature': ('django.db.models.fields.TextField', [], {}),
            'sms_mask': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'feedback.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Client']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'feedback': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'feedback'", 'max_length': '25'})
        }
    }

    complete_apps = ['feedback']
