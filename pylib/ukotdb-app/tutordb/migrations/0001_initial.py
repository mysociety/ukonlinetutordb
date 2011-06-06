# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Centre'
        db.create_table('tutordb_centre', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('tutordb', ['Centre'])

        # Adding model 'Tutor'
        db.create_table('tutordb_tutor', (
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('tutordb', ['Tutor'])

        # Adding model 'Tenure'
        db.create_table('tutordb_tenure', (
            ('tutor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutordb.Tutor'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('centre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutordb.Centre'])),
        ))
        db.send_create_signal('tutordb', ['Tenure'])

        # Adding unique constraint on 'Tenure', fields ['centre', 'tutor']
        db.create_unique('tutordb_tenure', ['centre_id', 'tutor_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Centre'
        db.delete_table('tutordb_centre')

        # Deleting model 'Tutor'
        db.delete_table('tutordb_tutor')

        # Deleting model 'Tenure'
        db.delete_table('tutordb_tenure')

        # Removing unique constraint on 'Tenure', fields ['centre', 'tutor']
        db.delete_unique('tutordb_tenure', ['centre_id', 'tutor_id'])
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tutordb.centre': {
            'Meta': {'object_name': 'Centre'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'tutordb.tenure': {
            'Meta': {'unique_together': "(('centre', 'tutor'),)", 'object_name': 'Tenure'},
            'centre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutordb.Centre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutordb.Tutor']"})
        },
        'tutordb.tutor': {
            'Meta': {'object_name': 'Tutor', '_ormbases': ['auth.User']},
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }
    
    complete_apps = ['tutordb']
