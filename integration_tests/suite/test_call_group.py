# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from hamcrest import has_properties

from .helpers.confd import MockContext, MockLine, MockUser
from .helpers.base import raw_cels, RawCelIntegrationTest
from .helpers.constants import USERS_TENANT


class TestCallToGroup(RawCelIntegrationTest):
    @raw_cels(
        '''\
 eventtype   |           eventtime           |     cid_name      |               cid_num                | cid_ani | cid_dnid |                exten                 |          context           |                               channame                                | appname  |                        appdata                        |   uniqueid    |   linkedid    | userfield |                         peer                         |                                          extra
-------------+-------------------------------+-------------------+--------------------------------------+---------+----------+--------------------------------------+----------------------------+-----------------------------------------------------------------------+----------+-------------------------------------------------------+---------------+---------------+-----------+------------------------------------------------------+------------------------------------------------------------------------------------------
CHAN_START   | 2021-08-23 15:06:41.605534-04 | Anastasia Romanov | 1011                                 |         |          | 2002                                 | inside                     | PJSIP/Ogrp1Zgu-00000007                                               |          |                                                       | 1629745601.28 | 1629745601.28 |           |                                                      |
APP_START    | 2021-08-23 15:06:41.686001-04 | Anastasia Romanov | 1011                                 | 1011    | 2002     | s                                    | group                      | PJSIP/Ogrp1Zgu-00000007                                               | Queue    | romanov,ir,,,,,,wazo-group-answered                   | 1629745601.28 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.693117-04 |                   |                                      |         |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;1 |          |                                                       | 1629745601.29 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.693205-04 |                   |                                      |         |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;2 |          |                                                       | 1629745601.30 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.693784-04 |                   |                                      |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;1 |          |                                                       | 1629745601.31 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.693818-04 |                   |                                      |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;2 |          |                                                       | 1629745601.32 | 1629745601.28 |           |                                                      |
APP_START    | 2021-08-23 15:06:41.74026-04  | Anastasia Romanov | 1011                                 | 1011    |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;2 | Dial     | sccp/fkwk2z0g                                         | 1629745601.30 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.740377-04 | Nikolai Romanov   | 1014                                 |         |          | s                                    | inside                     | SCCP/fkwk2z0g-00000003                                                |          |                                                       | 1629745601.33 | 1629745601.28 |           |                                                      |
APP_START    | 2021-08-23 15:06:41.913456-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;2 | Dial     | Local/TokxAXWb@wazo_wait_for_registration             | 1629745601.32 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.913574-04 |                   |                                      |         |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000b;1                  |          |                                                       | 1629745601.34 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:41.913618-04 |                   |                                      |         |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000b;2                  |          |                                                       | 1629745601.35 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:06:48.027422-04 | Olga Romanov      | 1015                                 |         |          | s                                    | inside                     | PJSIP/TokxAXWb-00000008                                               |          |                                                       | 1629745608.36 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.723848-04 | Nikolai Romanov   | 1014                                 |         |          | s                                    | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;1 | AppQueue | (Outgoing Line)                                       | 1629745601.29 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:06:56.723848-04 | Nikolai Romanov   | 1014                                 |         |          | s                                    | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;1 | AppQueue | (Outgoing Line)                                       | 1629745601.29 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.724567-04 |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;1 | AppQueue | (Outgoing Line)                                       | 1629745601.31 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:06:56.724567-04 |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;1 | AppQueue | (Outgoing Line)                                       | 1629745601.31 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.727071-04 | Nikolai Romanov   | 1014                                 |         |          | a545ea83-595d-4142-a40c-9012acd3068d | inside                     | SCCP/fkwk2z0g-00000003                                                | AppDial  | (Outgoing Line)                                       | 1629745601.33 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:06:56.727071-04 | Nikolai Romanov   | 1014                                 |         |          | a545ea83-595d-4142-a40c-9012acd3068d | inside                     | SCCP/fkwk2z0g-00000003                                                | AppDial  | (Outgoing Line)                                       | 1629745601.33 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.727657-04 | Anastasia Romanov | 1011                                 | 1011    |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;2 |          |                                                       | 1629745601.30 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":"CANCEL"}
CHAN_END     | 2021-08-23 15:06:56.727657-04 | Anastasia Romanov | 1011                                 | 1011    |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-00000009;2 |          |                                                       | 1629745601.30 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.728897-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000b;1                  | AppDial  | (Outgoing Line)                                       | 1629745601.34 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:06:56.728897-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000b;1                  | AppDial  | (Outgoing Line)                                       | 1629745601.34 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.729647-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;2 |          |                                                       | 1629745601.32 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":"CANCEL"}
CHAN_END     | 2021-08-23 15:06:56.729647-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000a;2 |          |                                                       | 1629745601.32 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.732326-04 | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000b;2                  |          |                                                       | 1629745601.35 | 1629745601.28 |           |                                                      | {"hangupcause":0,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:06:56.732326-04 | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000b;2                  |          |                                                       | 1629745601.35 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:06:56.92459-04  | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000008                                               | AppDial2 | (Outgoing Line)                                       | 1629745608.36 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:06:56.92459-04  | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000008                                               | AppDial2 | (Outgoing Line)                                       | 1629745608.36 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:01.727274-04 |                   |                                      |         |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;1 |          |                                                       | 1629745621.37 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:01.727535-04 |                   |                                      |         |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;2 |          |                                                       | 1629745621.38 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:01.729794-04 |                   |                                      |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;1 |          |                                                       | 1629745621.39 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:01.729978-04 |                   |                                      |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 |          |                                                       | 1629745621.40 | 1629745601.28 |           |                                                      |
APP_START    | 2021-08-23 15:07:01.851721-04 | Anastasia Romanov | 1011                                 | 1011    |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;2 | Dial     | sccp/fkwk2z0g                                         | 1629745621.38 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:01.851894-04 | Nikolai Romanov   | 1014                                 |         |          | s                                    | inside                     | SCCP/fkwk2z0g-00000004                                                |          |                                                       | 1629745621.41 | 1629745601.28 |           |                                                      |
APP_START    | 2021-08-23 15:07:02.030074-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 | Dial     | Local/TokxAXWb@wazo_wait_for_registration             | 1629745621.40 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:02.03021-04  |                   |                                      |         |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  |          |                                                       | 1629745622.42 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:02.030246-04 |                   |                                      |         |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2                  |          |                                                       | 1629745622.43 | 1629745601.28 |           |                                                      |
CHAN_START   | 2021-08-23 15:07:02.073465-04 | Olga Romanov      | 1015                                 |         |          | s                                    | inside                     | PJSIP/TokxAXWb-00000009                                               |          |                                                       | 1629745622.44 | 1629745601.28 |           |                                                      |
ANSWER       | 2021-08-23 15:07:04.122603-04 | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000009                                               | AppDial2 | (Outgoing Line)                                       | 1629745622.44 | 1629745601.28 |           |                                                      |
ANSWER       | 2021-08-23 15:07:04.442902-04 | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2                  | Stasis   | dial_mobile,dial,TokxAXWb                             | 1629745622.43 | 1629745601.28 |           |                                                      |
ANSWER       | 2021-08-23 15:07:04.444202-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |                                                      |
ANSWER       | 2021-08-23 15:07:04.444459-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 | Dial     | Local/TokxAXWb@wazo_wait_for_registration             | 1629745621.40 | 1629745601.28 |           |                                                      |
ANSWER       | 2021-08-23 15:07:04.444632-04 |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;1 | AppQueue | (Outgoing Line)                                       | 1629745621.39 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:07:04.444987-04 | Nikolai Romanov   | 1014                                 |         |          | s                                    | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;1 | AppQueue | (Outgoing Line)                                       | 1629745621.37 | 1629745601.28 |           |                                                      | {"hangupcause":26,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:07:04.444987-04 | Nikolai Romanov   | 1014                                 |         |          | s                                    | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;1 | AppQueue | (Outgoing Line)                                       | 1629745621.37 | 1629745601.28 |           |                                                      |
BRIDGE_ENTER | 2021-08-23 15:07:04.445739-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |                                                      | {"bridge_id":"95e497a6-4577-4c40-836a-259591dbd928","bridge_technology":"simple_bridge"}
BRIDGE_ENTER | 2021-08-23 15:07:04.44589-04  | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 | Dial     | Local/TokxAXWb@wazo_wait_for_registration             | 1629745621.40 | 1629745601.28 |           | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1 | {"bridge_id":"95e497a6-4577-4c40-836a-259591dbd928","bridge_technology":"simple_bridge"}
HANGUP       | 2021-08-23 15:07:04.446125-04 | Nikolai Romanov   | 1014                                 |         |          | a545ea83-595d-4142-a40c-9012acd3068d | inside                     | SCCP/fkwk2z0g-00000004                                                | AppDial  | (Outgoing Line)                                       | 1629745621.41 | 1629745601.28 |           |                                                      | {"hangupcause":26,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:07:04.446125-04 | Nikolai Romanov   | 1014                                 |         |          | a545ea83-595d-4142-a40c-9012acd3068d | inside                     | SCCP/fkwk2z0g-00000004                                                | AppDial  | (Outgoing Line)                                       | 1629745621.41 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:07:04.446243-04 | Anastasia Romanov | 1011                                 | 1011    |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;2 |          |                                                       | 1629745621.38 | 1629745601.28 |           |                                                      | {"hangupcause":26,"hangupsource":"","dialstatus":"CANCEL"}
CHAN_END     | 2021-08-23 15:07:04.446243-04 | Anastasia Romanov | 1011                                 | 1011    |          | a545ea83-595d-4142-a40c-9012acd3068d | usersharedlines            | Local/a545ea83-595d-4142-a40c-9012acd3068d@usersharedlines-0000000c;2 |          |                                                       | 1629745621.38 | 1629745601.28 |           |                                                      |
BRIDGE_ENTER | 2021-08-23 15:07:04.47732-04  | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000009                                               | Stasis   | dial_mobile,join,8517788a-4f6a-4134-a3ed-df0ef2285ae7 | 1629745622.44 | 1629745601.28 |           |                                                      | {"bridge_id":"8517788a-4f6a-4134-a3ed-df0ef2285ae7","bridge_technology":"simple_bridge"}
ANSWER       | 2021-08-23 15:07:04.48789-04  | Anastasia Romanov | 1011                                 | 1011    | 2002     | s                                    | group                      | PJSIP/Ogrp1Zgu-00000007                                               | Queue    | romanov,ir,,,,,,wazo-group-answered                   | 1629745601.28 | 1629745601.28 |           |                                                      |
BRIDGE_ENTER | 2021-08-23 15:07:04.489662-04 |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;1 | AppQueue | (Outgoing Line)                                       | 1629745621.39 | 1629745601.28 |           |                                                      | {"bridge_id":"dd9e89f4-9004-4cbe-9aff-1dd7cd2e2e2e","bridge_technology":"simple_bridge"}
BRIDGE_ENTER | 2021-08-23 15:07:04.489957-04 | Anastasia Romanov | 1011                                 | 1011    | 2002     | s                                    | group                      | PJSIP/Ogrp1Zgu-00000007                                               | Queue    | romanov,ir,,,,,,wazo-group-answered                   | 1629745601.28 | 1629745601.28 |           |                                                      | {"bridge_id":"dd9e89f4-9004-4cbe-9aff-1dd7cd2e2e2e","bridge_technology":"simple_bridge"}
BRIDGE_ENTER | 2021-08-23 15:07:04.4903-04   | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2                  | Stasis   | dial_mobile,dial,TokxAXWb                             | 1629745622.43 | 1629745601.28 |           | PJSIP/TokxAXWb-00000009                              | {"bridge_id":"8517788a-4f6a-4134-a3ed-df0ef2285ae7","bridge_technology":"simple_bridge"}
BRIDGE_EXIT  | 2021-08-23 15:07:04.496939-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |                                                      | {"bridge_id":"95e497a6-4577-4c40-836a-259591dbd928","bridge_technology":"simple_bridge"}
BRIDGE_EXIT  | 2021-08-23 15:07:04.497139-04 |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;1 | AppQueue | (Outgoing Line)                                       | 1629745621.39 | 1629745601.28 |           | PJSIP/Ogrp1Zgu-00000007                              | {"bridge_id":"dd9e89f4-9004-4cbe-9aff-1dd7cd2e2e2e","bridge_technology":"simple_bridge"}
BRIDGE_ENTER | 2021-08-23 15:07:04.497156-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           | PJSIP/Ogrp1Zgu-00000007                              | {"bridge_id":"dd9e89f4-9004-4cbe-9aff-1dd7cd2e2e2e","bridge_technology":"simple_bridge"}
BRIDGE_EXIT  | 2021-08-23 15:07:04.497449-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 | Dial     | Local/TokxAXWb@wazo_wait_for_registration             | 1629745621.40 | 1629745601.28 |           |                                                      | {"bridge_id":"95e497a6-4577-4c40-836a-259591dbd928","bridge_technology":"simple_bridge"}
HANGUP       | 2021-08-23 15:07:04.497603-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 |          |                                                       | 1629745621.40 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"","dialstatus":"ANSWER"}
CHAN_END     | 2021-08-23 15:07:04.497603-04 | Anastasia Romanov | 1011                                 | 1011    |          | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;2 |          |                                                       | 1629745621.40 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:07:04.49787-04  |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;1 | AppQueue | (Outgoing Line)                                       | 1629745621.39 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:07:04.49787-04  |                   | 2002                                 |         |          | s                                    | usersharedlines            | Local/3925098f-c504-4b7d-bf8a-499bb7cc4d92@usersharedlines-0000000d;1 | AppQueue | (Outgoing Line)                                       | 1629745621.39 | 1629745601.28 |           |                                                      |
BRIDGE_EXIT  | 2021-08-23 15:07:08.290905-04 | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000009                                               | Stasis   | dial_mobile,join,8517788a-4f6a-4134-a3ed-df0ef2285ae7 | 1629745622.44 | 1629745601.28 |           | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2 | {"bridge_id":"8517788a-4f6a-4134-a3ed-df0ef2285ae7","bridge_technology":"simple_bridge"}
HANGUP       | 2021-08-23 15:07:08.292471-04 | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000009                                               | AppDial2 | (Outgoing Line)                                       | 1629745622.44 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"PJSIP/TokxAXWb-00000009","dialstatus":""}
CHAN_END     | 2021-08-23 15:07:08.292471-04 | Anastasia Romanov | 1011                                 | 1011    |          | s                                    | inside                     | PJSIP/TokxAXWb-00000009                                               | AppDial2 | (Outgoing Line)                                       | 1629745622.44 | 1629745601.28 |           |                                                      |
BRIDGE_EXIT  | 2021-08-23 15:07:08.309629-04 | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2                  | Stasis   | dial_mobile,dial,TokxAXWb                             | 1629745622.43 | 1629745601.28 |           |                                                      | {"bridge_id":"8517788a-4f6a-4134-a3ed-df0ef2285ae7","bridge_technology":"simple_bridge"}
HANGUP       | 2021-08-23 15:07:08.312141-04 | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2                  |          |                                                       | 1629745622.43 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"PJSIP/TokxAXWb-00000009","dialstatus":""}
CHAN_END     | 2021-08-23 15:07:08.312141-04 | Anastasia Romanov | 1011                                 | 1011    |          | TokxAXWb                             | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;2                  |          |                                                       | 1629745622.43 | 1629745601.28 |           |                                                      |
BRIDGE_EXIT  | 2021-08-23 15:07:08.313285-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |                                                      | {"bridge_id":"dd9e89f4-9004-4cbe-9aff-1dd7cd2e2e2e","bridge_technology":"simple_bridge"}
BRIDGE_EXIT  | 2021-08-23 15:07:08.313468-04 | Anastasia Romanov | 1011                                 | 1011    | 2002     | s                                    | group                      | PJSIP/Ogrp1Zgu-00000007                                               | Queue    | romanov,ir,,,,,,wazo-group-answered                   | 1629745601.28 | 1629745601.28 |           |                                                      | {"bridge_id":"dd9e89f4-9004-4cbe-9aff-1dd7cd2e2e2e","bridge_technology":"simple_bridge"}
HANGUP       | 2021-08-23 15:07:08.31911-04  | Anastasia Romanov | 1011                                 | 1011    | 2002     | s                                    | group                      | PJSIP/Ogrp1Zgu-00000007                                               |          |                                                       | 1629745601.28 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"","dialstatus":"ANSWER"}
CHAN_END     | 2021-08-23 15:07:08.31911-04  | Anastasia Romanov | 1011                                 | 1011    | 2002     | s                                    | group                      | PJSIP/Ogrp1Zgu-00000007                                               |          |                                                       | 1629745601.28 | 1629745601.28 |           |                                                      |
HANGUP       | 2021-08-23 15:07:08.342721-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |                                                      | {"hangupcause":16,"hangupsource":"","dialstatus":""}
CHAN_END     | 2021-08-23 15:07:08.342721-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |                                                      |
LINKEDID_END | 2021-08-23 15:07:08.342721-04 |                   | 3925098f-c504-4b7d-bf8a-499bb7cc4d92 |         |          |                                      | wazo_wait_for_registration | Local/TokxAXWb@wazo_wait_for_registration-0000000e;1                  | AppDial  | (Outgoing Line)                                       | 1629745622.42 | 1629745601.28 |           |
        '''
    )
    def test_call_to_group_answered_by_a_pushed_mobile(self):
        user_1_uuid = '3925098f-c504-4b7d-bf8a-499bb7cc4d92'  # Olga
        user_2_uuid = 'a545ea83-595d-4142-a40c-9012acd3068d'  # Nikolai
        user_3_uuid = '10288506-4ad6-4052-8218-2aa133727e93'  # Anastasia
        self.confd.set_users(
            MockUser(user_1_uuid, USERS_TENANT, line_ids=[1]),
            MockUser(user_2_uuid, USERS_TENANT, line_ids=[2]),
            MockUser(user_3_uuid, USERS_TENANT, line_ids=[3]),
        )
        self.confd.set_lines(
            MockLine(
                id=1,
                name='TokxAXWb',
                users=[{'uuid': user_1_uuid}],
                tenant_uuid=USERS_TENANT,
                extensions=[{'exten': '1015', 'context': 'inside'}],
            ),
            MockLine(
                id=2,
                name='fkwk2z0g',
                users=[{'uuid': user_2_uuid}],
                tenant_uuid=USERS_TENANT,
                extensions=[{'exten': '1014', 'context': 'inside'}],
            ),
            MockLine(
                id=3,
                name='Ogrp1Zgu',
                users=[{'uuid': user_3_uuid}],
                tenant_uuid=USERS_TENANT,
                extensions=[{'exten': '1011', 'context': 'inside'}],
            ),
        )
        self.confd.set_contexts(
            MockContext(id=1, name='inside', tenant_uuid=USERS_TENANT)
        )

        self._assert_last_call_log_matches(
            '1629745601.28',
            has_properties(
                source_name='Anastasia Romanov',
                source_exten='1011',
                requested_exten='2002',
                destination_internal_exten='1015',
                destination_exten='1015',
                destination_name='Olga Romanov',
                destination_participant=has_properties(
                    user_uuid='3925098f-c504-4b7d-bf8a-499bb7cc4d92',
                )
            )
        )
