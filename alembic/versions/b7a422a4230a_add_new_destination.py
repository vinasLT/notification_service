"""add new destination

Revision ID: b7a422a4230a
Revises: 089551a8f7e3
Create Date: 2025-12-15 11:46:09.311857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7a422a4230a'
down_revision: Union[str, Sequence[str], None] = '089551a8f7e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to align enums with current models."""
    destination_values = ("email", "sms", "telegram")
    status_values = ("success", "in_progress", "failure")
    routing_key_values = (
        "auth.send_code",
        "auth.reset_password",
        "bid.new_bid_placed",
        "bid.you_won_bid",
        "bid.you_lost_bid",
        "order.status_updated",
    )

    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        destination_enum = sa.Enum(
            *destination_values, name="notificationdestination_new"
        )
        status_enum = sa.Enum(*status_values, name="notificationstatus_new")
        routing_enum = sa.Enum(
            *routing_key_values, name="notificationroutingkey_new"
        )

        destination_enum.create(bind, checkfirst=True)
        status_enum.create(bind, checkfirst=True)
        routing_enum.create(bind, checkfirst=True)

        op.execute("UPDATE notification SET destination = LOWER(destination)")
        op.execute(
            "UPDATE notification SET status = CASE "
            "WHEN status = 'SUCCESS' THEN 'success' "
            "WHEN status = 'IN_PROGRESS' THEN 'in_progress' "
            "WHEN status = 'FAILURE' THEN 'failure' "
            "ELSE status END"
        )
        op.execute(
            "UPDATE notification SET routing_key = CASE "
            "WHEN routing_key = 'AUTH_SEND_CODE' THEN 'auth.send_code' "
            "WHEN routing_key = 'AUTH_RESET_PASSWORD' THEN 'auth.reset_password' "
            "WHEN routing_key = 'NEW_BID_PLACED' THEN 'bid.new_bid_placed' "
            "WHEN routing_key = 'YOU_WON_BID' THEN 'bid.you_won_bid' "
            "WHEN routing_key = 'YOU_LOST_BID' THEN 'bid.you_lost_bid' "
            "WHEN routing_key = 'ORDER_STATUS_UPDATED' THEN 'order.status_updated' "
            "ELSE routing_key END"
        )

        op.execute(
            "ALTER TABLE notification ALTER COLUMN destination "
            "TYPE notificationdestination_new "
            "USING destination::text::notificationdestination_new"
        )
        op.execute(
            "ALTER TABLE notification ALTER COLUMN status "
            "TYPE notificationstatus_new "
            "USING status::text::notificationstatus_new"
        )
        op.execute(
            "ALTER TABLE notification ALTER COLUMN routing_key "
            "TYPE notificationroutingkey_new "
            "USING routing_key::text::notificationroutingkey_new"
        )

        op.execute("DROP TYPE IF EXISTS notificationdestination")
        op.execute("ALTER TYPE notificationdestination_new RENAME TO notificationdestination")
        op.execute("DROP TYPE IF EXISTS notificationstatus")
        op.execute("ALTER TYPE notificationstatus_new RENAME TO notificationstatus")
        op.execute("DROP TYPE IF EXISTS notificationroutingkey")
        op.execute("ALTER TYPE notificationroutingkey_new RENAME TO notificationroutingkey")
    else:
        op.execute("UPDATE notification SET destination = LOWER(destination)")
        op.execute(
            "UPDATE notification SET status = CASE "
            "WHEN status = 'SUCCESS' THEN 'success' "
            "WHEN status = 'IN_PROGRESS' THEN 'in_progress' "
            "WHEN status = 'FAILURE' THEN 'failure' "
            "ELSE status END"
        )
        op.execute(
            "UPDATE notification SET routing_key = CASE "
            "WHEN routing_key = 'AUTH_SEND_CODE' THEN 'auth.send_code' "
            "WHEN routing_key = 'AUTH_RESET_PASSWORD' THEN 'auth.reset_password' "
            "WHEN routing_key = 'NEW_BID_PLACED' THEN 'bid.new_bid_placed' "
            "WHEN routing_key = 'YOU_WON_BID' THEN 'bid.you_won_bid' "
            "WHEN routing_key = 'YOU_LOST_BID' THEN 'bid.you_lost_bid' "
            "WHEN routing_key = 'ORDER_STATUS_UPDATED' THEN 'order.status_updated' "
            "ELSE routing_key END"
        )

        destination_enum = sa.Enum(
            *destination_values, name="notificationdestination"
        )
        status_enum = sa.Enum(*status_values, name="notificationstatus")
        routing_enum = sa.Enum(
            *routing_key_values, name="notificationroutingkey"
        )

        with op.batch_alter_table("notification", recreate="always") as batch_op:
            batch_op.alter_column(
                "destination",
                existing_type=sa.String(),
                type_=destination_enum,
                existing_nullable=False,
            )
            batch_op.alter_column(
                "status",
                existing_type=sa.String(),
                type_=status_enum,
                existing_nullable=False,
            )
            batch_op.alter_column(
                "routing_key",
                existing_type=sa.String(),
                type_=routing_enum,
                existing_nullable=False,
            )


def downgrade() -> None:
    """Revert enums to the previous (uppercase) representation."""
    old_destination_values = ("EMAIL", "SMS")
    old_status_values = ("SUCCESS", "IN_PROGRESS", "FAILURE")
    old_routing_key_values = ("AUTH_SEND_CODE", "AUTH_RESET_PASSWORD")

    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        destination_enum = sa.Enum(
            *old_destination_values, name="notificationdestination_old"
        )
        status_enum = sa.Enum(
            *old_status_values, name="notificationstatus_old"
        )
        routing_enum = sa.Enum(
            *old_routing_key_values, name="notificationroutingkey_old"
        )

        destination_enum.create(bind, checkfirst=True)
        status_enum.create(bind, checkfirst=True)
        routing_enum.create(bind, checkfirst=True)

        op.execute("UPDATE notification SET destination = UPPER(destination)")
        op.execute(
            "UPDATE notification SET status = CASE "
            "WHEN status = 'success' THEN 'SUCCESS' "
            "WHEN status = 'in_progress' THEN 'IN_PROGRESS' "
            "WHEN status = 'failure' THEN 'FAILURE' "
            "ELSE status END"
        )
        op.execute(
            "UPDATE notification SET routing_key = CASE "
            "WHEN routing_key = 'auth.send_code' THEN 'AUTH_SEND_CODE' "
            "WHEN routing_key = 'auth.reset_password' THEN 'AUTH_RESET_PASSWORD' "
            "ELSE routing_key END"
        )

        op.execute(
            "ALTER TABLE notification ALTER COLUMN destination "
            "TYPE notificationdestination_old "
            "USING destination::text::notificationdestination_old"
        )
        op.execute(
            "ALTER TABLE notification ALTER COLUMN status "
            "TYPE notificationstatus_old "
            "USING status::text::notificationstatus_old"
        )
        op.execute(
            "ALTER TABLE notification ALTER COLUMN routing_key "
            "TYPE notificationroutingkey_old "
            "USING routing_key::text::notificationroutingkey_old"
        )

        op.execute("DROP TYPE IF EXISTS notificationdestination")
        op.execute("ALTER TYPE notificationdestination_old RENAME TO notificationdestination")
        op.execute("DROP TYPE IF EXISTS notificationstatus")
        op.execute("ALTER TYPE notificationstatus_old RENAME TO notificationstatus")
        op.execute("DROP TYPE IF EXISTS notificationroutingkey")
        op.execute("ALTER TYPE notificationroutingkey_old RENAME TO notificationroutingkey")
    else:
        op.execute("UPDATE notification SET destination = UPPER(destination)")
        op.execute(
            "UPDATE notification SET status = CASE "
            "WHEN status = 'success' THEN 'SUCCESS' "
            "WHEN status = 'in_progress' THEN 'IN_PROGRESS' "
            "WHEN status = 'failure' THEN 'FAILURE' "
            "ELSE status END"
        )
        op.execute(
            "UPDATE notification SET routing_key = CASE "
            "WHEN routing_key = 'auth.send_code' THEN 'AUTH_SEND_CODE' "
            "WHEN routing_key = 'auth.reset_password' THEN 'AUTH_RESET_PASSWORD' "
            "ELSE routing_key END"
        )

        destination_enum = sa.Enum(
            *old_destination_values, name="notificationdestination"
        )
        status_enum = sa.Enum(*old_status_values, name="notificationstatus")
        routing_enum = sa.Enum(
            *old_routing_key_values, name="notificationroutingkey"
        )

        with op.batch_alter_table("notification", recreate="always") as batch_op:
            batch_op.alter_column(
                "routing_key",
                existing_type=sa.String(),
                type_=routing_enum,
                existing_nullable=False,
            )
            batch_op.alter_column(
                "status",
                existing_type=sa.String(),
                type_=status_enum,
                existing_nullable=False,
            )
            batch_op.alter_column(
                "destination",
                existing_type=sa.String(),
                type_=destination_enum,
                existing_nullable=False,
            )
