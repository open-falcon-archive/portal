# -*- coding:utf-8 -*-
__author__ = 'Ulric Qin'
import logging
from frame.store import db
from web.model.host_group import HostGroup


def delete_group(group_id=None):
    try:
        cursor = db.execute('delete from grp where id = %s', [group_id])
        db.execute('delete from grp_host where grp_id = %s', [group_id], cursor=cursor)
        db.execute('delete from grp_tpl where grp_id = %s', [group_id], cursor=cursor)
        db.execute('delete from plugin_dir where grp_id = %s', [group_id], cursor=cursor)
        db.commit()
        return ''
    except Exception, e:
        logging.getLogger().error(e)
        db.rollback()
        return 'delete group %s fail' % group_id
    finally:
        cursor and cursor.close()


def rename(old_str=None, new_str=None, login_user=None):
    print(old_str, new_str, login_user)
    gs = HostGroup.select_vs(where='create_user = %s and come_from = %s', params=[login_user, 1])
    for g in gs:
        HostGroup.update_dict({'grp_name': g.grp_name.replace(old_str, new_str)}, 'id=%s', [g.id])
    return ''

