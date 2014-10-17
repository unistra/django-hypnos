from __future__ import unicode_literals

import keyword
import re
from django.core.management.base import NoArgsCommand, CommandError
from django.utils.datastructures import SortedDict
from django.conf import settings
from os.path import join
from django.db import connections


class Command(NoArgsCommand):
    help = "Create models, serializers, urls and views for the webservice"

    database = 'webservice'
    requires_model_validation = False
    db_module = 'django.db'
    app_folder = join(join(settings.DJANGO_ROOT, "apps"), "webservice")

    def table2model(self, table_name):
        return table_name.title().replace('_', '')\
                                 .replace(' ', '')\
                                 .replace('-', '')\


    def handle_noargs(self, **options):
        try:
            with open(join(self.app_folder, "models.py"), 'w') as f:
                for line in self.handle_inspection(options):
                    f.write("%s\n" % line)
            self.stdout.write("models.py:ok")
            with open(join(self.app_folder, "serializers.py"), 'w') as f:
                for line in self.handle_serializers(options):
                    f.write("%s\n" % line)
            self.stdout.write("serializers.py:ok")
            with open(join(self.app_folder, "views.py"), 'w') as f:
                for line in self.handle_views(options):
                    f.write("%s\n" % line)
            self.stdout.write("views.py:ok")
            with open(join(self.app_folder, "urls.py"), 'w') as f:
                for line in self.handle_urls(options):
                    f.write("%s\n" % line)
            self.stdout.write("urls.py:ok")
        except NotImplementedError:
            raise CommandError("Database inspection isn't supported for the \
currently selected database backend.")
        except Exception:
            raise CommandError("An error occured")
        else:
            self.stdout.write("Webservice created !")

    def handle_urls(self, options):
        connection = connections[self.database]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        cursor = connection.cursor()
        yield "# This is an auto-generated Django model module."
        yield ''
        yield "from rest_framework_fine_permissions.serializers \
import ModelPermissionsSerializer"
        yield 'from django.conf.urls import patterns, url'
        yield 'from rest_framework.urlpatterns import format_suffix_patterns'
        yield 'from . import views'
        yield ''
        yield "urlpatterns = patterns('',"

        for table_name in connection.introspection.table_names(cursor):
            if table_name_filter is not None and callable(table_name_filter):
                if not table_name_filter(table_name):
                    continue
            yield "url(r'^%s/(?P<pk>\d+)$', views.%sDetail.as_view(), \
name='%s-all-detail')," % (self.table2model(table_name).lower(),
                           self.table2model(table_name),
                           self.table2model(table_name).lower())
            yield "url(r'^%s$', views.%sList.as_view(), \
name='%s-all-list')," % (self.table2model(table_name).lower(),
                           self.table2model(table_name),
                           self.table2model(table_name).lower())
        yield ')'
        yield "urlpatterns = format_suffix_patterns(urlpatterns, \
suffix_required=True)"

    def handle_views(self, options):
        connection = connections[self.database]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        cursor = connection.cursor()
        yield "# This is an auto-generated Django model module."
        yield ''
        yield "from rest_framework_fine_permissions.serializers \
import ModelPermissionsSerializer"
        yield 'from . import models'
        yield 'from . import serializers'
        yield 'from rest_framework import generics'
        yield ''

        for table_name in connection.introspection.table_names(cursor):
            if table_name_filter is not None and callable(table_name_filter):
                if not table_name_filter(table_name):
                    continue
            yield 'class %sDetail(generics.RetrieveUpdateDestroyAPIView):' % (
                self.table2model(table_name),)
            yield "    model = models.%s" % self.table2model(table_name)
            yield "    serializer_class = serializers.%sSerializer\n" % (
                self.table2model(table_name),)
            yield 'class %sList(generics.ListCreateAPIView):' % (
                self.table2model(table_name),)
            yield "    queryset = models.%s.objects.all()" % self.table2model(table_name)
            yield "    serializer_class = serializers.%sSerializer\n" % (
                self.table2model(table_name),)

    def handle_serializers(self, options):
        connection = connections[self.database]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        cursor = connection.cursor()
        yield "# This is an auto-generated Django model module."
        yield ''
        yield "from rest_framework_fine_permissions.serializers \
import ModelPermissionsSerializer"
        yield 'from . import models'
        yield ''

        for table_name in connection.introspection.table_names(cursor):
            if table_name_filter is not None and callable(table_name_filter):
                if not table_name_filter(table_name):
                    continue
            yield 'class %sSerializer(ModelPermissionsSerializer):' % (
                self.table2model(table_name),)
            yield "    class Meta:"
            yield "        model = models.%s\n" % self.table2model(table_name)

    def handle_inspection(self, options):
        connection = connections[self.database]
        # 'table_name_filter' is a stealth option
        table_name_filter = options.get('table_name_filter')

        strip_prefix = lambda s: s[1:] if s.startswith("u'") else s

        cursor = connection.cursor()
        yield "# This is an auto-generated Django model module."
        yield "from __future__ import unicode_literals"
        yield ''
        yield 'from %s import models' % self.db_module
        yield ''
        known_models = []
        for table_name in connection.introspection.table_names(cursor):
            if table_name_filter is not None and callable(table_name_filter):
                if not table_name_filter(table_name):
                    continue
            yield 'class %s(models.Model):' % self.table2model(table_name)
            known_models.append(self.table2model(table_name))
            try:
                relations = connection.introspection.get_relations(
                    cursor, table_name)
            except NotImplementedError:
                relations = {}
            try:
                indexes = connection.introspection.get_indexes(
                    cursor, table_name)
            except NotImplementedError:
                indexes = {}
            # Holds column names used in the table so far
            used_column_names = []
            for i, row in enumerate(
                connection.introspection.get_table_description(cursor,
                                                               table_name)):
                # Holds Field notes, to be displayed in a Python comment.
                comment_notes = []
                # Holds Field parameters such as 'db_column'.
                extra_params = SortedDict()
                column_name = row[0]
                is_relation = i in relations

                att_name, params, notes = self.normalize_col_name(
                    column_name, used_column_names, is_relation)
                extra_params.update(params)
                comment_notes.extend(notes)

                used_column_names.append(att_name)

                # Add primary_key and unique, if necessary.
                if column_name in indexes:
                    if indexes[column_name]['primary_key']:
                        extra_params['primary_key'] = True
                    elif indexes[column_name]['unique']:
                        extra_params['unique'] = True

                if is_relation:
                    rel_to = "self" if relations[i][
                        1] == table_name else self.table2model(relations[i][1])
                    if rel_to in known_models:
                        field_type = 'ForeignKey(%s' % rel_to
                    else:
                        field_type = "ForeignKey('%s'" % rel_to
                else:
                    # Calling `get_field_type` to get the field type string
                    # and any additional paramters and notes.
                    field_type, field_params, \
                        field_notes = self.get_field_type(
                            connection, table_name, row)
                    extra_params.update(field_params)
                    comment_notes.extend(field_notes)

                    field_type += '('

                # Don't output 'id = meta.AutoField(primary_key=True)', because
                # that's assumed if it doesn't exist.
                if att_name == 'id' and field_type == 'AutoField(' and \
                   extra_params == {'primary_key': True}:
                    continue

                # Add 'null' and 'blank', if the 'null_ok' flag was present
                # in the table description.
                if row[6]:  # If it's NULL...
                    if field_type == 'BooleanField(':
                        field_type = 'NullBooleanField('
                    else:
                        extra_params['blank'] = True
                        if not field_type in ('TextField(', 'CharField('):
                            extra_params['null'] = True

                field_desc = '%s = models.%s' % (att_name, field_type)
                if extra_params:
                    if not field_desc.endswith('('):
                        field_desc += ', '
                    field_desc += ', '.join([
                        '%s=%s' % (k, strip_prefix(repr(v)))
                        for k, v in extra_params.items()])
                field_desc += ')'
                if comment_notes:
                    field_desc += ' # ' + ' '.join(comment_notes)
                yield '    %s' % field_desc
            for meta_line in self.get_meta(table_name):
                yield meta_line

    def normalize_col_name(self, col_name, used_column_names, is_relation):
        """
        Modify the column name to make it Python-compatible as a field name
        """
        field_params = {}
        field_notes = []

        new_name = col_name.lower()
        if new_name != col_name:
            field_notes.append('Field name made lowercase.')

        if is_relation:
            if new_name.endswith('_id'):
                new_name = new_name[:-3]
            else:
                field_params['db_column'] = col_name

        new_name, num_repl = re.subn(r'\W', '_', new_name)
        if num_repl > 0:
            field_notes.append(
                'Field renamed to remove unsuitable characters.')

        if new_name.find('__') >= 0:
            while new_name.find('__') >= 0:
                new_name = new_name.replace('__', '_')
            if col_name.lower().find('__') >= 0:
                # Only add the comment if the double underscore was in the
                # original name
                field_notes.append(
                    "Field renamed because it contained more than one '_' \
in a row.")

        if new_name.startswith('_'):
            new_name = 'field%s' % new_name
            field_notes.append("Field renamed because it started with '_'.")

        if new_name.endswith('_'):
            new_name = '%sfield' % new_name
            field_notes.append("Field renamed because it ended with '_'.")

        if keyword.iskeyword(new_name):
            new_name += '_field'
            field_notes.append(
                'Field renamed because it was a Python reserved word.')

        if new_name[0].isdigit():
            new_name = 'number_%s' % new_name
            field_notes.append(
                "Field renamed because it wasn't a valid Python identifier.")

        if new_name in used_column_names:
            num = 0
            while '%s_%d' % (new_name, num) in used_column_names:
                num += 1
            new_name = '%s_%d' % (new_name, num)
            field_notes.append('Field renamed because of name conflict.')

        if col_name != new_name and field_notes:
            field_params['db_column'] = col_name

        return new_name, field_params, field_notes

    def get_field_type(self, connection, table_name, row):
        """
        Given the database connection, the table name, and the cursor row
        description, this routine will return the given field type name, as
        well as any additional keyword parameters and notes for the field.
        """
        field_params = SortedDict()
        field_notes = []

        try:
            field_type = connection.introspection.get_field_type(row[1], row)
        except KeyError:
            field_type = 'TextField'
            field_notes.append('This field type is a guess.')

        # This is a hook for DATA_TYPES_REVERSE to return a tuple of
        # (field_type, field_params_dict).
        if type(field_type) is tuple:
            field_type, new_params = field_type
            field_params.update(new_params)

        # Add max_length for all CharFields.
        if field_type == 'CharField' and row[3]:
            field_params['max_length'] = int(row[3]) if row[3] > 0 else 255

        if field_type == 'DecimalField':
            if row[4] is None or row[5] is None:
                field_notes.append(
                    'max_digits and decimal_places have been guessed, as this '
                    'database handles decimal fields as float')
                field_params['max_digits'] = row[
                    4] if row[4] is not None else 10
                field_params['decimal_places'] = row[
                    5] if row[5] is not None else 5
            else:
                field_params['max_digits'] = row[4]
                field_params['decimal_places'] = row[5]

        return field_type, field_params, field_notes

    def get_meta(self, table_name):
        """
        Return a sequence comprising the lines of code necessary
        to construct the inner Meta class for the model corresponding
        to the given database table name.
        """
        return ["    class Meta:",
                "        managed = False",
                "        db_table = '%s'" % table_name,
                "        permissions = (('view_%s', 'Can view %s'),)" %
                (self.table2model(table_name).lower(),
                 self.table2model(table_name).lower()),
                ""]
