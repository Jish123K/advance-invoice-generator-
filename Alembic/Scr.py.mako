from jinja2 import Template

import sqlalchemy as sa

# revision identifiers, used by Alembic.

revision = {{ repr(up_revision) }}

down_revision = {{ repr(down_revision) }}

branch_labels = {{ repr(branch_labels) }}

depends_on = {{ repr(depends_on) }}

# define the template string

template_str = """{{ message }}

Revision ID: {{ up_revision }}

Revises: {{ down_revision | join(',', True) if down_revision else None }}

Create Date: {{ create_date }}

"""

# compile the template

template = Template(template_str)

def upgrade():

    ${upgrades if upgrades else "pass"}

def downgrade():

    ${downgrades if downgrades else "pass"}

# render the template and execute the resulting SQL

sql = template.render(

    message="",

    up_revision=up_revision,

    down_revision=down_revision,

    create_date=sa.func.current_timestamp(),

    join=','.join,

)

# execute the SQL using Alembic's `op` object

with op.batch_alter_table("my_table") as batch_op:

    batch_op.execute(sql)

