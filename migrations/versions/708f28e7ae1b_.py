"""Add DB layer constraints for the data models

Revision ID: 708f28e7ae1b
Revises: 01bbd1772553
Create Date: 2022-09-10 13:03:33.330095

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '708f28e7ae1b'
down_revision = '01bbd1772553'
branch_labels = None
depends_on = None


def upgrade():
    # ### manually created constraints since alembic do not recognize constraints written
    # on models automatically:

    # creative model constraints:
    op.create_check_constraint("check_width_positive", "creative", "width > 0")
    op.create_check_constraint("check_height_positive", "creative", "height > 0")

    # line_item model constraints
    op.create_check_constraint("check_max_impressions_positive", "line_item", "max_impressions > 0")
    op.create_check_constraint("check_rpm_positive", "line_item", "rpm > 0")

    op.create_check_constraint("check_start_before_end", "line_item", "campaign_end > campaign_start")

    # ### end Alembic commands ###


def downgrade():
    # remove constraints:

    # creative model constrants:
    op.drop_constraint("check_width_positive", "creative", type_="check")


    # line_item model constraints
    op.drop_constraint("check_max_impressions_positive", "line_item", type_="check")
    op.drop_constraint("check_rpm_positive", "line_item",  type_="check")

    op.drop_constraint("check_start_before_end", "line_item", type_="check")
