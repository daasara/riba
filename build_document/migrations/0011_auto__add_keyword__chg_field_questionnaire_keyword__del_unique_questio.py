# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Keyword'
        db.create_table('build_document_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['build_document.Template'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
        ))
        db.send_create_signal('build_document', ['Keyword'])

        # Renaming column for 'Questionnaire.keyword' to match new field type.
        db.rename_column('build_document_questionnaire', 'keyword', 'keyword_id')
        # Changing field 'Questionnaire.keyword'
        db.alter_column('build_document_questionnaire', 'keyword_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['build_document.Keyword'], null=True, blank=True))

        # Removing unique constraint on 'Questionnaire', fields ['question', 'keyword']
        #db.delete_unique('build_document_questionnaire', ['question_id', 'keyword'])


    def backwards(self, orm):
        
        # Deleting model 'Keyword'
        db.delete_table('build_document_keyword')

        # Renaming column for 'Questionnaire.keyword' to match new field type.
        db.rename_column('build_document_questionnaire', 'keyword_id', 'keyword')
        # Changing field 'Questionnaire.keyword'
        db.alter_column('build_document_questionnaire', 'keyword', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Adding unique constraint on 'Questionnaire', fields ['question', 'keyword']
        db.create_unique('build_document_questionnaire', ['question_id', 'keyword'])


    models = {
        'build_document.keyword': {
            'Meta': {'unique_together': "(('template', 'keyword'),)", 'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build_document.Template']"})
        },
        'build_document.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build_document.Keyword']", 'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['question.Question']", 'null': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['build_document.Template']"})
        },
        'build_document.template': {
            'Meta': {'object_name': 'Template'},
            'about': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['categories.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'list_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'offer_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20', 'db_index': 'True', 'blank': 'True'}),
            'time_to_build': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'upload_document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'upload_text': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'})
        },
        'categories.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'question.question': {
            'Meta': {'object_name': 'Question'},
            'answer_type': ('django.db.models.fields.CharField', [], {'default': "'char'", 'max_length': '15', 'db_index': 'True'}),
            'columns': ('django.db.models.fields.IntegerField', [], {'default': '40', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'rows': ('django.db.models.fields.IntegerField', [], {'default': '5', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '10', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['build_document']