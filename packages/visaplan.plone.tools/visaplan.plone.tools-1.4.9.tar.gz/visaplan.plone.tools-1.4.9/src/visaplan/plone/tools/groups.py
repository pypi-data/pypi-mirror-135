# -*- coding: utf-8 -*- äöü vim: ts=8 sts=4 sw=4 si et hls tw=79
"""
Tools for groups
"""

# Python compatibility:
from __future__ import absolute_import, print_function

from six import iteritems as six_iteritems
from six import text_type as six_text_type

# Zope:
from Products.CMFCore.utils import getToolByName

# visaplan:
from visaplan.tools.lands0 import list_of_strings

# Local imports:
from visaplan.plone.tools.context import make_translator

try:
    # visaplan:
    from visaplan.tools.coding import safe_decode
except ImportError:
    if __name__ != '__main__':
        raise
    def safe_decode(s):
        if isinstance(s, six_text_type):
            return s
        return s.decode('utf-8')

__all__ = [
	# function factories:
	'groupinfo_factory',
	'is_direct_member__factory',
	'is_member_of__factory',
        # used directly:
	'is_member_of_any',
	'get_all_members',  # verbose info; calls:
	# helpers:
        'recursive_members',  # operates on any dict
	'split_group_id',
	'build_groups_set',
	'_traverse_dict',
	]

# -------------------------------- [ groupinfo_factory ... [
def groupinfo_factory(context, pretty=0, forlist=0, searchtext=0):
    """
    Factory-Funktion; als Ersatz für get_group_info_by_id, insbesondere für
    wiederholte Aufrufe.  Indirektionen etc. werden einmalig beim Erstellen der
    Funktion aufgelöst und anschließend in einer Closure vorgehalten.

    pretty -- Gruppennamen auflösen, wenn Suffix an ID und Titel
    forlist -- Minimale Rückgabe (nur ID und Titel),
               aber mit pretty kombinierbar
    """
    pg = getToolByName(context, 'portal_groups')
    get_group = pg.getGroupById
    acl = getToolByName(context, 'acl_users')
    translate = make_translator(context)
    GROUPS = acl.source_groups._groups

    def minimal_group_info(group_id):
        """
        Nur ID und Titel
        """
        group = get_group(group_id)

        dict_ = {'id': group_id}
        try:
            thegroup = GROUPS[group_id]
            dict_['group_title'] = safe_decode(thegroup['title'])
            return dict_
        except KeyError:
            return {}

    def basic_group_info(group_id):
        """
        Gib ein Dict. zurück;
        - immer vorhandene Schlüssel:
          id, group_title, group_description, group_manager, group_desktop
        - nur bei automatisch erzeugten Gruppen: role, role_translation, brain

        Argumente:
        group_id -- ein String, normalerweise mit 'group_' beginnend
        """

        group = get_group(group_id)

        dict_ = {'id': group_id}
        try:
            thegroup = GROUPS[group_id]
            dict_['group_title'] = safe_decode(thegroup['title'])
        except KeyError:
            return {}
        dict_['group_description'] = safe_decode(thegroup['description'])
        dict_['group_manager'] = thegroup.get('group_manager')
        dict_['group_desktop'] = thegroup.get('group_desktop')

        dic = split_group_id(group_id)
        if dic['role'] is not None:
            dict_.update(dic)

        dict_['role_translation'] = translate(dic['role'])
        dict_['brain'] = getbrain(context, dic['uid'])
        return dict_

    def pretty_group_info(group_id):
        """
        Ruft basic_group_info auf und fügt einen Schlüssel 'pretty_title'
        hinzu, der den Gruppentitel ohne das Rollensuffix enthält.
        """
        dic = basic_group_info(group_id)
        try:
            if 'role' not in dic:
                dic['pretty_title'] = translate(dic['group_title'])
                return dic
            liz = dic['group_title'].split()
            if liz and liz[-1] == dic['role']:
                stem = u' '.join(liz[:-1])
                mask = PRETTY_MASK[dic['role']]
                dic['pretty_title'] = translate(mask).format(group=stem)
            else:
                dic['pretty_title'] = translate(dic['group_title'])
        except KeyError as e:
            # evtl. keine Gruppe! (Aufruf durch get_mapping_group)
            print(e)
            pass
        return dic

    def minimal2_group_info(group_id):
        """
        Ruft minimal_group_info auf und modifiziert ggf. den Schlüssel
        'group_title' (entsprechend dem von pretty_group_info zurückgegebenen
        Schlüssel 'pretty_title')
        """
        dic = minimal_group_info(group_id)
        if not dic:     # Gruppe nicht (mehr) gefunden;
            return dic  # {} zurückgeben
        dic2 = split_group_id(group_id)
        if dic2['role'] is not None:
            dic.update(dic2)
        if 'role' not in dic:
            dic['group_title'] = translate(dic['group_title'])
            return dic
        liz = dic['group_title'].split()
        if liz and liz[-1] == six_text_type(dic['role']):
            stem = u' '.join(liz[:-1])
            mask = PRETTY_MASK[dic['role']]
            dic['group_title'] = translate(mask).format(group=stem)
        else:
            dic['group_title'] = translate(dic['group_title'])
        return dic

    def make_searchstring(group_info):
        """
        Arbeite direkt auf einem group_info-Dict;
        Gib kein Dict zurück, sondern einen String für Suchzwecke
        """
        try:
            group_id = group_info['id']
        except KeyError:
            raise
        try:
            res = [safe_decode(group_info['title']),
                   safe_decode(group_id)]
        except KeyError:
            print(list(group_info.items()))
            raise
            return u''
        dic2 = split_group_id(group_id)
        prettify = True
        for val in dic2.values():
            if val is None:
                prettify = False
                break  # es sind immer alle None, oder alle nicht None
            else:
                res.append(safe_decode(val))
        if prettify:
            pretty = pretty_group_title(group_id, res[0], translate)
            if pretty is not None:
                res.append(safe_decode(pretty))
        descr = group_info['description']
        if descr:
            res.append(safe_decode(descr))
        return u' '.join(res)

    if searchtext:
        return make_searchstring
    if forlist:
        if pretty:
            return minimal2_group_info
        else:
            return minimal_group_info
    if pretty:
        return pretty_group_info
    else:
        return basic_group_info
# -------------------------------- ] ... groupinfo_factory ]


# --------------------------------- [ userinfo_factory ... [
def userinfo_factory(context, pretty=0, forlist=0,
                     title_or_id=0):
    """
    Wie groupinfo_factory, aber für Benutzerobjekte.

    pretty -- für Benutzer: title als formatierter Name
              (author.get_formatted_name), wenn möglich
    forlist -- Minimale Rückgabe (nur ID und Titel),
               aber mit pretty kombinierbar
    title_or_id -- für Verwendung mit visaplan.tools.classes.Proxy:
               gib nur den Title oder ersatzweise die ID zurück
               (mit pretty kombinierbar)
    """
    acl = getToolByName(context, 'acl_users')
    acl_gu = acl.getUser
    if pretty or not forlist:
        author = context.restrictedTraverse('@@author', None)
        gbbuid = author.getBrainByUserId
        gfn = author.get_formatted_name

    # ---------------------------- [ forlist ... [
    def basic_user_info(member_id):
        """
        Basisinformationen über einen Benutzer:
        id, title

        forlist, not: pretty
        """
        member = acl_gu(member_id)
        if member:
            return {'id': member_id,
                    'title': member.getProperty('fullname'),
                    }

    def pretty_user_info(member_id):
        """
        Basisinformationen über einen Benutzer:
        id, title

        forlist, pretty
        """
        member = acl_gu(member_id)
        if member:
            brain = gbbuid(member_id)
            return {'id': member_id,
                    'title': (brain and gfn(brain))
                             or member.getProperty('fullname'),
                    }
    # ---------------------------- ] ... forlist ]

    # ------------------------ [ title_or_id ... [
    def pretty_title_or_id(member_id):
        try:
            return pretty_user_info(member_id)['title'] \
                   or member_id
        except:
            return None

    def basic_title_or_id(member_id):
        try:
            return basic_user_info(member_id)['title'] \
                   or member_id
        except:
            return None
    # ------------------------ ] ... title_or_id ]

    def full_user_info(member_id):
        """
        not: forlist, not: pretty
        """
        member = acl_gu(member_id)
        if member:
            brain = gbbuid(member_id)
            return {'id': member_id,
                    'title': member.getProperty('fullname'),
                    'brain': brain,
                    'email': member.getProperty('email'),
                    }

    def full_pretty_user_info(member_id):
        """
        not: forlist, pretty
        """
        member = acl_gu(member_id)
        if member:
            brain = gbbuid(member_id)
            return {'id': member_id,
                    'title': (brain and gfn(brain))
                             or member.getProperty('fullname'),
                    'brain': brain,
                    'email': member.getProperty('email'),
                    }

    if title_or_id:
        if pretty:
            return pretty_title_or_id
        else:
            return basic_title_or_id
    if forlist:
        if pretty:
            return pretty_user_info
        else:
            return basic_user_info
    if pretty:
        return full_pretty_user_info
    else:
        return full_user_info
# --------------------------------- ] ... userinfo_factory ]


def is_direct_member__factory(context, userid):
    """
    Erzeuge eine Funktion, die prüft, ob der *beim Erzeugen angegebene* Nutzer
    in der bei jedem Aufruf anzugebenden Gruppe direkt enthalten ist.
    """
    acl = getToolByName(context, 'acl_users')
    gpm = acl.source_groups._group_principal_map

    def is_direct_member_of(group_id):
        return userid in gpm[group_id]

    return is_direct_member_of


def is_member_of__factory(context, userid):
    """
    Erzeuge eine Funktion, die die *direkte oder indirekte* Mitgliedschaft
    des übergebenen Users in der jeweils zu übergebenden Gruppe überprüft.
    """
    acl = getToolByName(context, 'acl_users')
    gpm = acl.source_groups._group_principal_map

    groups = build_groups_set(gpm, userid)

    def is_member_of(groupid):
        return groupid in groups

    return is_member_of


def is_member_of_any(context, group_ids, user_id=None, default=False):
    """
    Is the given or active user member of one of the given groups?

    - For anonymous execution, raises Unauthorized
      (might become changable by keyword-only argument)
    - The normal usage is without specification of the user_id,
      i.e. checking for the logged-in user
    - if the group_ids sequence is empty, the default is used

    """
    pm = getToolByName(context, 'portal_membership')
    if pm.isAnonymousUser():
        raise Unauthorized
    if user_id is not None:
        # wer darf sowas fragen? Manager, Gruppenmanager, ...?
        # TODO: Hier entsprechende Überprüfung!
        pass

    if not group_ids:
        return default
    if user_id is None:
        member = pm.getAuthenticatedMember()
        user_id = member.getId()

    return user_id in get_all_members(context, group_ids)


def get_all_members(context, group_ids, **kwargs):  # --- [[
    """
    Return all members of the given groups

    Liefere alle Mitglieder der übergebenen Gruppe(n).

    Schlüsselwortargumente für .utils.recursive_members und
    groupinfo_factory dürfen angegeben werden;
    letztere werden aber ignoriert, wenn die vorgabegemäße Filterung
    groups_only=True übersteuert wird. In diesem Fall (potentiell sowohl
    Benutzer als auch Gruppen, oder nur Benutzer) werden nur IDs
    zurückgegeben.

    Rückgabe:
    - Sequenz von Gruppeninformationen, mit groups_only=True (Vorgabe);
    - ansonsten nur eine Sequenz der IDs (je nach Aufrufargumenten nur
      Benutzer-IDs, oder gemischt)
    """
    acl = getToolByName(context, 'acl_users')
    gpm = acl.source_groups._group_principal_map
    filter_args = {}
    for key in ('groups_only', 'users_only',
		'containers',
		'default_to_all'):
	try:
	    filter_args[key] = kwargs.pop(key)
	except KeyError:
	    pass
    members = recursive_members(list_of_strings(group_ids),
				gpm, **filter_args)
    groups_only = filter_args.get('groups_only', False)
    if groups_only:
	format_args = {'pretty': False,
		       'forlist': True,
		       }
	format_args.update(kwargs)
	ggibi = groupinfo_factory(context, **format_args)
	res = []
	for gid in members:
	    res.append(ggibi(gid))
	return res
    elif kwargs and debug_active:
	pp('ignoriere:', kwargs)

    return members
# ---------------------------------- ] ... get_all_members ]


# --------------------------------- [ helper functions ... [
def recursive_members(gids, dic,
                      containers=None,
                      groups_only=False,
                      users_only=False,
                      default_to_all=False):
    """
    Recursively find all members of the (by id) given groups.

    Mandatory arguments:

      gids -- group ids; a sequence or (for convenience) a string
              (which would be split by whitespace)
      dic -- a dictionary; usually acl.source_groups._group_principal_map

    Ermittle die rekursiv aufgelösten Mitglieder der übergebenen
    Gruppen.

    >>> dic = {'group_a': ['group_b', 'group_c'],
    ...        'group_b': ['user_a', 'user_b'],
    ...        'group_c': ['user_c'],
    ...        'group_d': ['group_a'],
    ...        }
    >>> am = recursive_members(['group_a'], dic, groups_only=True)
    >>> sorted(am)
    ['group_b', 'group_c']
    >>> sorted(recursive_members(['group_a'], dic))
    ['group_b', 'group_c', 'user_a', 'user_b', 'user_c']
    >>> sorted(recursive_members(['group_d'], dic, users_only=True))
    ['user_a', 'user_b', 'user_c']
    >>> sorted(recursive_members(['group_d'], dic, groups_only=True))
    ['group_a', 'group_b', 'group_c']

    containers-Argument:
    - True: die Container werden hinzugefügt
      (mit groups_only: ... sofern es wirklich Gruppen sind)
    - False: die Container werden ausgefiltert
    - None (Vorgabe): weder aktiv hinzufügen noch ausfiltern

    >>> kwargs = {'groups_only': True,
    ...           'containers': True}
    >>> sorted(recursive_members(['group_d'], dic, **kwargs))
    ['group_a', 'group_b', 'group_c', 'group_d']
    >>> kwargs = {'groups_only': True,
    ...           'containers': False}
    >>> sorted(recursive_members(['group_c', 'group_d'], dic, **kwargs))
    ['group_a', 'group_b']
    >>> kwargs = {'users_only': True,
    ...           'containers': True}
    >>> sorted(recursive_members(['group_d'], dic, **kwargs))
    ['user_a', 'user_b', 'user_c']
    >>> kwargs = {'containers': False}

    Das spezielle Argument default_to_all erfordert groups_only=True
    und gibt alle Gruppen zurück, sofern keine Gruppen-IDs übergeben wurden:

    >>> sorted(recursive_members([], dic, groups_only=True,
    ...                          default_to_all=True))
    ['group_a', 'group_b', 'group_c', 'group_d']
    """
    if users_only and groups_only:
        raise ValueError('recursive_members(%(gids)r): '
                         '*either* groups_only '
                         '*or* users_only!'
                         % locals())
    if not gids:
        if default_to_all:
            assert groups_only, 'default_to_all erfordert groups_only!'
            return set(dic.keys())
        else:
            # ohne default_to_all: keine Gruppen, keine Mitglieder
            return set()
    filtered = users_only or groups_only
    res = set()
    exclude = set()
    if containers is None:
        pass
    elif not containers:
        exclude.update(gids)
    for gid in gids:
        try:
            newly_found = set(dic[gid]).difference(res)
            if containers and not users_only:
                res.add(gid)
        except KeyError:  # keine Gruppe, oder?!
            if containers and not groups_only:
                res.add(gid)
        else:
            while newly_found:
                res.update(newly_found)
                this_iteration = set()
                for mid in newly_found:  # member id
                    try:
                        found_here = set(dic[mid]).difference(res)
                        if found_here:
                            this_iteration.update(found_here)
                        if users_only:   # Gruppen aus Ergebnis entfernen
                            exclude.add(mid)
                    except KeyError:
                        if groups_only:  # Benutzer aus Ergebnis entfernen
                            exclude.add(mid)
                res.update(this_iteration)
                newly_found = this_iteration
    res.difference_update(exclude)
    return res


def split_group_id(gid, resolve_role=False):
    """
    Splitte die übergebene Gruppen-ID auf und gib ein Dictionary zurück,
    das über eine etwaige "Rollenkomponente" informiert und dann auch
    die uid des zugehörigen Objekts enthält.

    Achtung:
        Der Schlüssel 'role' enthält bisher nicht wirklich den Namen der
        Rolle, sondern das Suffix, das von diesem in wichtigen Fällen abweicht!
        Um dies zu beheben, resolve_role=True übergeben;
        dies schreibt nach 'role' die *real zu verwendende* Rolle,
        und das Suffix steht im zusätzlichen Schlüssel 'suffix'.

        In einer späteren Version wird der Vorgabewert von resolve_role auf
        True geändert, und noch etwas später die Unterstützung für False
        entfernt.

    Zunächst die Tests für resolve_role=False:

    Die Schlüssel 'uid' und 'role' haben String-Werte,
    sofern der Mittelteil wie eine korrekte UID aussieht und das Suffix
    eine der hierfür bekannten Rollen ist;
    ansonsten sind sie None.

    >>> split_group_id('group_f6350ab731c3601e925eac482206bda5_Author')
    {'role': 'Author', 'uid': 'f6350ab731c3601e925eac482206bda5'}

    Bei "normalen" Gruppen hat die scheinbare (!) UID keine spezielle
    Bedeutung und wird daher nicht als solche zurückgegeben:

    >>> split_group_id('group_0123456789abcdef0123456789abcdef')
    {'role': None, 'uid': None}

    Das Suffix 'learner' repräsentiert keine echte Rolle (es wird stattdessen
    'Reader' vermittelt); es ist aber ein bekanntes Suffix
    und wird (mit resolve_role=False) als 'role' zurückgegeben
    (mit resolve_role=True als 'suffix'; siehe unten):

    >>> split_group_id('group_f6350ab731c3601e925eac482206bda5_learner')
    {'role': 'learner', 'uid': 'f6350ab731c3601e925eac482206bda5'}

    Wenn Unicode übergeben wird, kommt Unicode zurück:

    >>> split_group_id(u'group_f6350ab731c3601e925eac482206bda5_Author')
    {'role': u'Author', 'uid': u'f6350ab731c3601e925eac482206bda5'}

    Es wird genau auf Plausibilität geprüft und ggf. ein Dict. mit
    None-Werten zurückgegeben.

    Falsche Zeichen in der UID:
    >>> split_group_id('group_FOOBARBAZ1c3601e925eac482206bda5_Author')
    {'role': None, 'uid': None}

    Unbekanntes oder leeres Suffix:
    >>> split_group_id('group_f6350ab731c3601e925eac482206bda5_')
    {'role': None, 'uid': None}
    >>> split_group_id('group_f6350ab731c3601e925eac482206bda5_Foo')
    {'role': None, 'uid': None}

    Falsche Länge der UID:
    >>> split_group_id('group_f6350ab731c3601c482206bda5_Author')
    {'role': None, 'uid': None}

    Falsches Präfix:
    >>> split_group_id('gröup_f6350ab731c3601e925eac482206bda5_learner')
    {'role': None, 'uid': None}
    >>> split_group_id(u'gröup_f6350ab731c3601e925eac482206bda5_learner')
    {'role': None, 'uid': None}

    Nun ergänzend noch Tests für resolve_role=True:

    >>> def sgi(gid):
    ...     return sorted(split_group_id(gid, resolve_role=True).items())
    >>> sgi('group_0123456789abcdef0123456789abcdef')
    [('role', None), ('suffix', None), ('uid', None)]

    >>> sgi('group_f6350ab731c3601e925eac482206bda5_Reader')
    [('role', 'Reader'), ('suffix', 'Reader'), ('uid', 'f6350ab731c3601e925eac482206bda5')]
    >>> sgi('group_f6350ab731c3601e925eac482206bda5_Author')
    [('role', 'Editor'), ('suffix', 'Author'), ('uid', 'f6350ab731c3601e925eac482206bda5')]
    >>> sgi('group_f6350ab731c3601e925eac482206bda5_learner')
    [('role', 'Reader'), ('suffix', 'learner'), ('uid', 'f6350ab731c3601e925eac482206bda5')]

    Die Alumni-Gruppe vermittelt keine Rolle direkt auf dem betroffenen Objekt;
    daher ist die Rolle hier None:
    >>> sgi('group_f6350ab731c3601e925eac482206bda5_alumni')
    [('role', None), ('suffix', 'alumni'), ('uid', 'f6350ab731c3601e925eac482206bda5')]

    """
    liz = gid.split('_', 2)
    if resolve_role:
        res = dict(RESOLVED_GROUP_INFO)
    else:
        res = dict(SIMPLE_GROUP_INFO)

    if not liz[2:]:
        return res
    elif liz[0] != 'group':
        return res
    elif liz[2] not in ALL_GROUP_SUFFIXES:
        return res
    uid = liz[1]
    if not uid:
        return res
    elif set(uid).difference(UID_CHARS):
        return res
    elif len(uid) != 32:
        return res
    res['uid'] = uid
    if resolve_role:
        res['suffix'] = suffix = liz[2]
        res['role'] = SUFFIX2ROLE[suffix]
    else:
        res['role'] = liz[2]
    return res


def build_groups_set(dic, userid):
    """
    Hilfsfunktion für is_member_of_factory

    >>> dic = {'group_a': ['group_b', 'group_c'],
    ...        'group_b': ['user_a', 'user_b'],
    ...        'group_c': ['user_c'],
    ...        }
    >>> groups = build_groups_set(dic, 'user_a')
    >>> sorted(groups)
    ['group_a', 'group_b', 'user_a']
    """
    groups = set([userid])
    _traverse_dict(dic, groups)
    return groups


def _traverse_dict(dic, groups):
    """
    Hilfsfunktion für build_groups_set:
    realisiert die Rekursion.
    Es wird abgebrochen, wenn es keine Änderungen mehr gab.

    >>> dic = {'group_a': ['group_b', 'group_c'],
    ...        'group_b': ['user_a', 'user_b'],
    ...        'group_c': ['user_c'],
    ...        }

    <groups> enthält zunächst die <uid> (oder gid) selbst:
    >>> groups = set(['user_a'])

    Der Rückgabewert wird üblicherweise nicht verwendet;
    er gibt die Anzahl der Iterationen an:
    >>> _traverse_dict(dic, groups)
    2
    >>> sorted(groups)
    ['group_a', 'group_b', 'user_a']
    """
    iterations = 1
    while True:
        finished = True
        for gid, members in six_iteritems(dic):
            if gid in groups:
                continue
            if groups.intersection(members):
                groups.add(gid)
                finished = False
        if finished:
            break
        iterations += 1
    return iterations
# --------------------------------- ] ... helper functions ]
