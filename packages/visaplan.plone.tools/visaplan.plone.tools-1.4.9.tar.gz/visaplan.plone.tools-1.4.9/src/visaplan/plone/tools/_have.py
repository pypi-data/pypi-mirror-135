# detect optional packages

# Python compatibility:
from __future__ import absolute_import

# Setup tools:
import pkg_resources

try:
    pkg_resources.get_distribution('beautifulsoup4')
except pkg_resources.DistributionNotFound:
    HAS_BEAUTIFULSOUP = False
else:
    HAS_BEAUTIFULSOUP = True

try:
    pkg_resources.get_distribution('plone.app.blob')
except pkg_resources.DistributionNotFound:
    HAS_BLOB = False
else:
    HAS_BLOB = True

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True

try:
    pkg_resources.get_distribution('Products.Archetypes')
except pkg_resources.DistributionNotFound:
    HAS_ARCHETYPES = False
else:
    HAS_ARCHETYPES = True

try:
    pkg_resources.get_distribution('visaplan.kitchen')
except pkg_resources.DistributionNotFound:
    HAS_KITCHEN = False
else:
    HAS_KITCHEN = True

try:
    pkg_resources.get_distribution('visaplan.plone.infohubs')
except pkg_resources.DistributionNotFound:
    HAS_INFOHUBS = False
else:
    HAS_INFOHUBS = True

try:
    pkg_resources.get_distribution('visaplan.plone.subportals')
except pkg_resources.DistributionNotFound:
    HAS_SUBPORTALS = False
else:
    HAS_SUBPORTALS = True

try:
    pkg_resources.get_distribution('visaplan.plone.search')
except pkg_resources.DistributionNotFound:
    HAS_VPSEARCH = False
else:
    HAS_VPSEARCH = True

try:
    pkg_resources.get_distribution('zope.i18n')
except pkg_resources.DistributionNotFound:
    HAS_ZOPE_I18N = False
else:
    HAS_ZOPE_I18N = True
