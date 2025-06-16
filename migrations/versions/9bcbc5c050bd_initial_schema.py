"""Initial schema

Revision ID: 9bcbc5c050bd
Revises: 
Create Date: 2025-06-16 21:58:34.179609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bcbc5c050bd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    -- Utmato Database Schema (extracted from PRD)

    -- Enable pgcrypto for UUID generation
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";

    -- Table for Organizations
    CREATE TABLE organizations (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        domain VARCHAR(255) UNIQUE NOT NULL,
        subscription_id VARCHAR(255), -- Stripe Subscription ID
        subscription_status VARCHAR(50) DEFAULT 'trialing', -- e.g., trialing, active, canceled
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    -- Enable RLS and add example policy for organizations
    ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
    CREATE POLICY org_select ON organizations
    FOR SELECT USING (true); -- TODO: Replace with org-based logic

    -- Table for Users
    CREATE TABLE users (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        clerk_user_id VARCHAR(255) UNIQUE NOT NULL,
        organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
        email VARCHAR(255) UNIQUE NOT NULL,
        role VARCHAR(50) NOT NULL CHECK (role IN ('Manager', 'Team Member')),
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    ALTER TABLE users ENABLE ROW LEVEL SECURITY;
    CREATE POLICY users_select ON users
    FOR SELECT USING (true); -- TODO: Replace with org/user-based logic

    -- Table for Campaigns
    CREATE TABLE campaigns (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
        created_by_user_id UUID NOT NULL REFERENCES users(id),
        name VARCHAR(255) NOT NULL,
        objective TEXT,
        audience_details JSONB, -- Stores targeting criteria
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
    CREATE POLICY campaigns_select ON campaigns
    FOR SELECT USING (true); -- TODO: Replace with org/user-based logic

    -- Table for UTM Links
    CREATE TABLE links (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
        created_by_user_id UUID NOT NULL REFERENCES users(id),
        destination_url TEXT NOT NULL,
        utm_source VARCHAR(255) NOT NULL,
        utm_medium VARCHAR(255) NOT NULL,
        utm_campaign VARCHAR(255) NOT NULL,
        utm_content VARCHAR(255),
        utm_term VARCHAR(255),
        full_url TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );
    ALTER TABLE links ENABLE ROW LEVEL SECURITY;
    CREATE POLICY links_select ON links
    FOR SELECT USING (true); -- TODO: Replace with org/user-based logic

    -- Table for Invitations
    CREATE TABLE invitations (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
        email VARCHAR(255) NOT NULL,
        token VARCHAR(255) UNIQUE NOT NULL,
        status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'expired')),
        expires_at TIMESTAMPTZ NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        UNIQUE(organization_id, email) -- Prevent duplicate pending invites
    ); 
    ALTER TABLE invitations ENABLE ROW LEVEL SECURITY;
    CREATE POLICY invitations_select ON invitations
    FOR SELECT USING (true); -- TODO: Replace with org/user-based logic """
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
