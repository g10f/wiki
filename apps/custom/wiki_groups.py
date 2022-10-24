# -*- coding: utf-8 -*-
"""
Group Backend wich checks the groups of the user roles from the SSO backend
The Group name is the Role name + 'Group'

for example,

SSO Role,    Wiki Group

Staff,       StaffGroup
Admin,       AdminGroup


"""

from MoinMoin.datastruct.backends import BaseGroupsBackend, GroupDoesNotExistError


class SSOGroups(BaseGroupsBackend):
    def group_pattern(self):
        try:
            return self.request.cfg.group_name
        except AttributeError:
            return u'%sGroup'

    def role_from_group_name(self, group_name):
        match = self.page_group_regex.search(group_name)
        if match:
            return match.groupdict()['key']

    def __contains__(self, group_name):
        role = self.role_from_group_name(group_name)
        if role and getattr(self.request.user, 'roles', None):
            return role in self.request.user.roles
        else:
            return False

    def __iter__(self):
        group_pattern = self.group_pattern()
        if getattr(self.request.user, 'roles', None):
            for role in self.request.user.roles:
                yield group_pattern % role

    def __getitem__(self, group_name):
        if group_name in self:
            return [self.request.user.name]
        else:
            raise GroupDoesNotExistError(group_name)
