# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sqlalchemy as sa

from sqlalchemy import distinct
from sqlalchemy import sql, func, and_
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import subqueryload

from .base import BaseDAO
from ..models import CallLog as CallLogSchema, CallLogParticipant


class CallLogDAO(BaseDAO):

    searched_columns = (
        CallLogSchema.source_name,
        CallLogSchema.source_exten,
        CallLogSchema.destination_name,
        CallLogSchema.destination_exten,
    )

    def get_by_id(self, cdr_id, tenant_uuids):
        with self.new_session() as session:
            query = session.query(CallLogSchema).options(
                joinedload('participants'),
                subqueryload('source_participant'),
                subqueryload('destination_participant'),
            )
            query = self._apply_filters(query, {'tenant_uuids': tenant_uuids})
            query = query.filter(CallLogSchema.id == cdr_id)
            cdr = query.one_or_none()
            if cdr:
                session.expunge_all()
                return cdr

    def find_all_in_period(self, params):
        with self.new_session() as session:
            query = self._list_query(session, params)
            order_field = None
            if params.get('order'):
                if params['order'] == 'marshmallow_duration':
                    order_field = CallLogSchema.date_end - CallLogSchema.date_answer
                elif params['order'] == 'marshmallow_answered':
                    order_field = CallLogSchema.date_answer
                else:
                    order_field = getattr(CallLogSchema, params['order'])
            if params.get('direction') == 'desc':
                order_field = order_field.desc().nullslast()
            if params.get('direction') == 'asc':
                order_field = order_field.asc().nullsfirst()
            if order_field is not None:
                query = query.order_by(order_field)

            if params.get('limit'):
                query = query.limit(params['limit'])
            if params.get('offset'):
                query = query.offset(params['offset'])

            call_log_rows = query.all()

            if not call_log_rows:
                return []

            session.expunge_all()

            return call_log_rows

    def _list_query(self, session, params):
        distinct_ = params.get('distinct')
        if distinct_ == 'peer_exten':
            # TODO(pcm) use the most recent call log not the most recent id
            sub_query = (
                session.query(func.max(CallLogParticipant.call_log_id).label('max_id'))
                .group_by(CallLogParticipant.user_uuid, CallLogParticipant.peer_exten)
                .subquery()
            )

            query = session.query(CallLogSchema).join(
                sub_query, and_(CallLogSchema.id == sub_query.c.max_id)
            )
        else:
            query = session.query(CallLogSchema)

        query = query.options(
            joinedload('participants'),
            subqueryload('source_participant'),
            subqueryload('destination_participant'),
        )

        query = self._apply_user_filter(query, params)
        query = self._apply_filters(query, params)
        return query

    def count_in_period(self, params):
        with self.new_session() as session:
            query = session.query(CallLogSchema)
            query = self._apply_user_filter(query, params)

            segregation_fields = ('tenant_uuids', 'me_user_uuid')
            count_params = dict([(p, params.get(p)) for p in segregation_fields])
            query = self._apply_filters(query, count_params)

            total = query.count()

            session.expunge_all()

            subquery = self._list_query(session, params).subquery()
            filtered = session.query(func.count(distinct(subquery.c.id))).scalar()

        return {'total': total, 'filtered': filtered}

    def _apply_user_filter(self, query, params):
        if params.get('me_user_uuid'):
            me_user_uuid = params['me_user_uuid']
            query = query.filter(
                CallLogSchema.participant_user_uuids.contains(str(me_user_uuid))
            )
        return query

    def _apply_filters(self, query, params):
        if params.get('start'):
            query = query.filter(CallLogSchema.date >= params['start'])
        if params.get('end'):
            query = query.filter(CallLogSchema.date < params['end'])

        if params.get('call_direction'):
            query = query.filter(CallLogSchema.direction == params['call_direction'])

        if params.get('id'):
            query = query.filter(CallLogSchema.id == params['id'])

        if params.get('search'):
            filters = (
                sql.cast(column, sa.String).ilike('%%%s%%' % params['search'])
                for column in self.searched_columns
            )
            query = query.filter(sql.or_(*filters))

        if params.get('number'):
            sql_regex = params['number'].replace('_', '%')
            filters = (
                sql.cast(column, sa.String).like('%s' % sql_regex)
                for column in [
                    CallLogSchema.source_exten,
                    CallLogSchema.destination_exten,
                ]
            )
            query = query.filter(sql.or_(*filters))

        for tag in params.get('tags', []):
            query = query.filter(
                CallLogSchema.participants.any(
                    CallLogParticipant.tags.contains(sql.cast([tag], ARRAY(sa.String)))
                )
            )

        if params.get('tenant_uuids'):
            query = query.filter(CallLogSchema.tenant_uuid.in_(params['tenant_uuids']))

        if params.get('me_user_uuid'):
            me_user_uuid = params['me_user_uuid']
            query = query.filter(
                CallLogSchema.participant_user_uuids.contains(str(me_user_uuid))
            )

        if params.get('user_uuids'):
            filters = (
                CallLogSchema.participant_user_uuids.contains(str(user_uuid))
                for user_uuid in params['user_uuids']
            )
            query = query.filter(sql.or_(*filters))

        if params.get('start_id'):
            query = query.filter(CallLogSchema.id >= params['start_id'])

        return query

    def create_from_list(self, call_logs):
        if not call_logs:
            return

        with self.new_session() as session:
            for call_log in call_logs:
                session.add(call_log)
                session.flush()
                # NOTE(fblackburn): fetch relationship before expunge_all
                call_log.source_participant
                call_log.destination_participant
            session.expunge_all()

    def delete_from_list(self, call_log_ids):
        with self.new_session() as session:
            query = session.query(CallLogSchema)
            query = query.filter(CallLogSchema.id.in_(call_log_ids))
            query.delete(synchronize_session=False)

    def delete(self, older=None):
        with self.new_session() as session:
            # NOTE(fblackburn) returning object on DELETE is specific to postgresql
            query = CallLogSchema.__table__.delete().returning(CallLogSchema.id)
            if older:
                query = query.where(CallLogSchema.date >= older)
            result = [r.id for r in session.execute(query)]
            return result
