from .. import db


class Conversation(db.Model):
    """ Conversation Model for storing user's chat and bot's generated responses """

    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text(), nullable=False)
    sender = db.Column(db.Text(), nullable=False)
    generated_on = db.Column(db.DateTime, nullable=False)
    response = db.Column(db.Text(), nullable=True, default="")

    def __repr__(self):
        return "<Conversation '{}'>".format(self.response)
