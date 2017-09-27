import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
# import model class
from app.models.user_ticket import UserTicket
from app.models.user import User
from app.builders.response_builder import ResponseBuilder
from app.models.ticket_transfer_log import TicketTransferLog


class TicketTransferService():

    def get_logs(self, user_id=''):
        if user_id == '':
            transferslogs = db.session.query(TicketTransferLog).all()
        else:
            transferslogsends = db.session.query(TicketTransferLog).filter(
                TicketTransferLog.sender_user_id == user_id)
            transferslogreceives = db.session.query(TicketTransferLog).filter(
                TicketTransferLog.sender_user_id == user_id)
            transferslogs = transferslogsends.union(transferslogreceives)

        return transferslogs

    def transfer(self, user_id, user_ticket_id, receiver):
        response = ResponseBuilder()
        userticket = db.session.query(UserTicket).filter_by(id=user_ticket_id)
        if userticket.first() is None:
            return response.set_error(True).set_data(None).set_message('ticket not found').build()

        if userticket.first().as_dict()['user_id'] != user_id:
            return response.set_error(True).set_data(None).set_message('this ticket is not yours').build()

        receiver_raw = db.session.query(User).filter(or_(User.username.like(receiver), User.email.like(receiver))).first()

        if receiver_raw is None:
            return response.set_error(True).set_data(None).set_message('receiver could not be found').build()
        receiver_id = receiver_raw.as_dict()['id']
        try:
            # update user ticket
            userticket.update({
                'user_id': receiver_id,
                'updated_at': datetime.datetime.now()
            })
            db.session.commit()

            # add transfer log
            transferlog = TicketTransferLog()
            transferlog.sender_user_id = user_id
            transferlog.receiver_user_id = receiver_id
            # transferlog.user_ticket_id = 1
            transferlog.user_ticket_id = user_ticket_id
            db.session.add(transferlog)

            db.session.commit()
            data = transferlog.as_dict()
            return response.set_data(data).set_message('ticket transfered successfully').build()

        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(None).set_message(data).set_error(True).build()
