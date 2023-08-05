"""
Interactive BLOBs cleanup,
inspired by a grok.view by Mikko Ohtamaa for Plone 4.1 and Dexterity 1.1;
see:

- https://stackoverflow.com/questions/8655675/cleaning-up-poskeyerror-no-blob-file-content-from-plone-site
- https://pypi.org/project/experimental.gracefulblobmissing/

The original script depended on five.grok and deleted affected objects without
further interaction; any interesting output was written to stdout.

Here we create an HTML table first, listing the objects with broken blob
data attributes in @@check-blobs;
in a second step, @@check-blobs-delete-selected can be called to delete the
checked objects.

TODO:
- Allow to clear the affected fields only.
- move to visaplan.plone.browsers @@management
- breadcrumbs
- return messages in a list
"""

# Python compatibility:
from __future__ import absolute_import

# Standard library:
from collections import Counter
from datetime import timedelta
from time import time

# Zope:
import transaction
from Products.CMFCore.interfaces import IFolderish, IPropertiesTool
from Products.Five.browser import BrowserView
# Zope imports
from ZODB.POSException import POSKeyError
from zope.component import getMultiAdapter, queryUtility

# Local imports:
from visaplan.plone.tools._have import HAS_ARCHETYPES, HAS_BLOB, HAS_DEXTERITY
from visaplan.plone.tools.context import getMessenger

# Logging / Debugging:
from logging import getLogger

interesting_at_fields = []

if HAS_ARCHETYPES:
    # Zope:
    from Products.Archetypes.Field import FileField, ImageField
    from Products.Archetypes.interfaces import IBaseContent
    interesting_at_fields.append(FileField)
    interesting_at_fields.append(ImageField)

if HAS_BLOB:
    # Plone:
    from plone.app.blob.subtypes.file import \
        ExtensionBlobField as FileExtensionBlobField
    from plone.app.blob.subtypes.image import \
        ExtensionBlobField as ImageExtensionBlobField
    interesting_at_fields.append(FileExtensionBlobField)
    interesting_at_fields.append(ImageExtensionBlobField)

if HAS_DEXTERITY:
    # Plone:
    from plone.dexterity.content import DexterityContent
    from plone.namedfile.interfaces import INamedFile

interesting_at_fields = tuple(interesting_at_fields)
log = getLogger('fix-blobs')


class FixBlobs(BrowserView):
    """
    A management view to clean up content with damaged BLOB files

    You can call this view by

    1) Starting Plone in debug mode (console output available)

    2) Visit site.com/@@check-blobs URL

    """

    def __init__(self, *args, **kwargs):
        BrowserView.__init__(self, *args, **kwargs)
        self.count = Counter()
        self.broken = []

    # ------------------------------ [ original code by Mikko Ohtamaa ... [
    def disable_integrity_check(self):
        """  Content HTML may have references to this broken image - we cannot fix that HTML
        but link integriry check will yell if we try to delete the bad image.

        http://collective-docs.readthedocs.org/en/latest/content/deleting.html#bypassing-link-integrity-check "
        """
        ptool = queryUtility(IPropertiesTool)
        props = getattr(ptool, 'site_properties', None)
        self.old_check = props.getProperty('enable_link_integrity_checks', False)
        props.enable_link_integrity_checks = False

    def restore_integrity_check_value(self):
        """
        Restore the original value
        """
        ptool = queryUtility(IPropertiesTool)
        props = getattr(ptool, 'site_properties', None)
        props.enable_link_integrity_checks = self.old_check
    # ------------------------------ ] ... original code by Mikko Ohtamaa ]

    def check_blobs(self):
        """
        Check for broken objects and return a Python dict, featuring the keys

        'count' - a Counter {'broken': x, 'inspected': x}

        'broken' - a list of dicts ('path', 'portal_type', 'modified',
                  'created', 'title')
        """
        count = self.count
        self.log_period = 1000
        self.start = time()
        _progress = []
        if HAS_ARCHETYPES:
            log.info('Archetypes framework support found (AT)')
            _progress.append('AT: %(at_objects_broken)2d broken'
                             ' / %(at_objects_checked)6d checked')
        else:
            log.info('NO Archetypes framework support found (AT)')
        if HAS_DEXTERITY:
            log.info('Dexterity framework support found (DX)')
            _progress.append('DX: %(dx_objects_broken)2d broken'
                             ' / %(dx_objects_checked)6d checked')
        else:
            log.info('NO Dexterity framework support found (DX)')
        if _progress:
            self.progress_mask = '; '.join(_progress)
        else:
            txt = 'No supported content framework found!'
            log.error(txt)
            return {
                'count': self.count,
                'broken': self.broken,
                'error': txt,
                }
        portal = self.context
        log.info('Checking objects below %(portal)r for broken BLOBs ...',
                 locals())
        self.recursively_check(portal)
        checked_total = count['objects_checked']
        if checked_total % self.log_period:
            log.info(self.progress_mask % count)
        bogus = count['unchecked_unknown']
        if bogus:
            log.warn('%(bogus)d objects not checked (unknown framework)',
                     locals())
        broken_total = count['objects_broken']
        if broken_total:
            for i, dic in enumerate(self.broken, 1):
                self.log_broken(dic, i, broken_total)

        log.info('DONE: Checked %(checked_total)d objects below %(portal)r.',
                 locals())
        total = timedelta(seconds=float(time() - self.start))
        log.info('Total time: %(total)s', locals())
        return {
            'count': self.count,
            'broken': self.broken,
            }

    def log_broken(self, dic, i, total):
        liz = ['BROKEN [%d/%d]:' % (i, total)]
        for key in ('path', 'portal_type', 'title', 'created', 'modified'):
            val = dic.get(key)
            if val:
                liz.append('%(key)s=%(val)r' % locals())
        log.error(' '.join(liz))

    def _check_blobs_of(self, o):
        count = self.count
        cnt_key = 'objects_checked'
        try:
            if HAS_ARCHETYPES and IBaseContent.providedBy(o):
                return self._check_at_blobs_of(o)
            elif HAS_DEXTERITY and isinstance(o, DexterityContent):
                return self._check_dx_blobs_of(o)
            else:
                cnt_key = 'unchecked_unknown'
                logger.warn('Can\'t check %(o)r: unknown framework',
                            locals())
                return
        finally:
            count[cnt_key] += 1
            count['objects_total'] += 1
            if not (count['objects_total'] % self.log_period):
                log.info(self.progress_mask % count)

    def _check_at_blobs_of(self, context):
        count = self.count
        schema = context.Schema()
        fields_checked = 0
        fields_broken = 0
        url = None
        for field in schema.fields():
            name = field.getName()
            if isinstance(field, interesting_at_fields):
                fields_checked += 1
                try:
                    field.get_size(context)
                except POSKeyError:
                    field_cls = field.__class__.__name__
                    if url is None:
                        url = context.absolute_url()
                        dic = {
                            'path': context.absolute_url_path(),
                            }
                    log.error("Found damaged AT %(field_cls)s %(name)r on %(url)s",
                              locals())
                    fields_broken += 1

        count['at_objects_checked'] += 1
        count['at_fields_checked'] += fields_checked
        if fields_broken:
            count['objects_broken'] += 1
            count['at_objects_broken'] += 1
            count['at_fields_broken'] += fields_broken
            try:
                ti = context.Title()
            except Exception as e:
                log.error('Error %(e)r getting the title of %(context)r!',
                          locals())
                ti = None
            dic.update({
                'title': ti,
                'created': context.created(),
                'modified': context.modified(),  # changed
                'portal_type': context.portal_type,
                })
            self.broken.append(dic)
            return True
        else:
            return False

    def _check_dx_blobs_of(self, context):
        """
        XXX: NOT TESTED - THEORETICAL, GUIDELINING, IMPLEMENTATION
        """

        count = self.count
        fields_checked = 0
        fields_broken = 0
        url = None

        # Iterate through all Python object attributes
        # XXX: Might be smarter to use zope.schema introspection here?
        for key, value in context.__dict__.items():
            # Ignore non-contentish attributes to speed up us a bit
            if not key.startswith("_"):
                if INamedFile.providedBy(value):
                    try:
                        value.getSize()
                    except POSKeyError:
                        if url is None:
                            url = context.absolute_url()
                            dic = {
                                'path': context.absolute_url_path(),
                                }
                        log.error("Found damaged Dexterity plone.app.NamedFile"
                                  " %(key)r on %(url)s",
                                  locals())
                        fields_broken += 1

        count['dx_objects_checked'] += 1
        count['dx_fields_checked'] += fields_checked
        if fields_broken:
            count['objects_broken'] += 1
            count['dx_objects_broken'] += 1
            count['dx_fields_broken'] += fields_broken
            try:
                ti = context.Title()
            except Exception as e:
                log.error('Error %(e)r getting the title of %(context)r!',
                          locals())
                ti = None
            dic.update({
                'title': ti,
                'created': context.created(),
                'modified': context.modified(),  # changed
                'portal_type': context.portal_type,
                })
            self.broken.append(dic)
            return True
        else:
            return False

    def recursively_check(self, folder):
        """
        Traverse the Plone site and collect information about objects with
        broken blobs
        """
        for id, child in folder.contentItems():

            self._check_blobs_of(child)

            if IFolderish.providedBy(child):
                self.recursively_check(child)

    def delete_selected(self):
        """
        Expect a list of paths in the 'delpath' variable;
        The given objects are checked again and, if indeed faulty,
        are deleted.
        """
        count = self.count = Counter()
        request = self.request
        delinquents = request.get('delpath', [])
        portal = self.context
        message = getMessenger(portal)
        notfound = []
        if not delinquents:
            message('Nothing to do', 'error')
            return count

        self.disable_integrity_check()
        done = False
        try:
            for delpa in delinquents:
                try:
                    spec = delpa
                    if spec.startswith('/'):
                        spec = spec.lstrip('/')
                    if not spec:
                        log.error('Invalid specification: %(delpa)r', locals())
                        count['invalid'] += 1
                        continue
                    o = portal.restrictedTraverse(spec)
                    if self._check_blobs_of(o):
                        # Yup, we have an error here:
                        o_pa = o.aq_parent
                        o_id = o.getId()
                        o_pa.manage_delObjects([o_id])
                        log.info('%(o_pa)r: deleted %(o)r', locals())
                        count['deleted'] += 1
                    else:
                        count['not_deleted'] += 1
                except KeyError:
                    notfound.append(delpa)
                    count['not_found'] += 1
            transaction.commit()
            done = True
        finally:
            self.restore_integrity_check_value()
            if done:
                log.info('Completed normally.')
            if count['deleted']:
                message('Checked and deleted ${deleted} object(s)',
                        mapping=count)
            if count['not_deleted']:
                message('No errors found for ${not_deleted} object(s)',
                        'warning',
                        mapping=count)
            if count['not_found']:
                message('${not_found} object(s) not found (already deleted?)',
                        'warning',
                        mapping=count)
            return count


