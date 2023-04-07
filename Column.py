from sqlalchemy import MetaData, Table, Column, Boolean, text

metadata = MetaData()

invoices = Table(

    'invoices',

    metadata,

    Column('id', sa.Integer, primary_key=True),

    # existing columns...

)

def upgrade():

    # create the new 'paid' column

    paid = Column('paid', Boolean, nullable=False, server_default=text('false'))

    paid.create(invoices)

def downgrade():

    # drop the 'paid' column

    paid = invoices.c.paid

    paid.drop()

