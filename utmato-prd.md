
# Utmato Product Requirements Document

## Document Control

| Document Information |                                        |
|----------------------|----------------------------------------|
| Document Title       | Utmato Product Requirements Document   |
| Version              | 1.1                                    |
| Status               | Revised Draft                          |
| Date                 | May 18, 2024                           |

## Table of Contents

1. [Introduction](#introduction)
2. [Product overview](#product-overview)
3. [Goals and objectives](#goals-and-objectives)
4. [Target audience](#target-audience)
5. [Features and requirements](#features-and-requirements)
6. [User stories and acceptance criteria](#user-stories-and-acceptance-criteria)
7. [Technical Epics / Non-Functional Requirements](#technical-epics--non-functional-requirements)
8. [Technical requirements / stack](#technical-requirements--stack)
9. [Design and user interface](#design-and-user-interface)

## Introduction

This Product Requirements Document (PRD) outlines the specifications and requirements for Utmato, a SaaS tool designed to help marketing teams plan, create, and track marketing campaigns with improved targeting and link management capabilities. The document serves as a comprehensive guide for the development team to understand the product's functionality, features, and technical specifications.

The PRD aims to define clear requirements for each feature, establish acceptance criteria, and provide a framework for development and testing. It will serve as the primary reference throughout the development lifecycle and provide transparency to all stakeholders involved in the project.

## Product overview

Utmato is a marketing campaign management platform that simplifies campaign planning, targeting, and tracking for marketing teams. The platform focuses on two key areas in its first phase:

1.  **Campaign setup with advanced targeting**: Enabling marketers to define campaigns and map them to precise audience targeting parameters (e.g., demographics, location, interests) to improve campaign performance and documentation.

2.  **Centralized UTM link management**: Providing a unified system for creating, managing, and tracking campaign links with standardized UTM parameters for consistent attribution and analytics.

Utmato offers a subscription-based service with both monthly and yearly billing options, team collaboration features, and a central dashboard for campaign oversight. The platform serves as a single source of truth for marketing teams to organize their digital campaigns across multiple platforms while maintaining consistent tracking and targeting parameters.

## Goals and objectives

### Primary goals

1.  Simplify campaign planning and metadata management for marketing teams.
2.  Streamline the creation, management, and storage of UTM-tagged links, standardizing them across different channels.
3.  Provide a centralized platform for managing campaign audience and targeting definitions.
4.  Enable effective team collaboration for managing campaign assets and metadata.

### Success criteria

1.  Successful implementation of all V1 core features defined in this PRD.
2.  Ability to handle at least 500 concurrent users with no performance degradation.
3.  99.9% uptime for the production environment.
4.  Conversion rate of 5% or higher from free trial to paid subscription within 6 months of launch.
5.  Average session duration of at least 15 minutes, indicating sustained user engagement.

## Target audience

### Primary audience

1.  **Marketing Managers**: Professionals responsible for planning, executing, and overseeing marketing campaigns across multiple channels. They require tools to organize campaign information, track performance, and ensure consistent implementation of marketing strategies.

2.  **Digital Marketers / Campaign Managers**: Specialists focused on implementing and optimizing digital marketing initiatives who need efficient ways to manage campaign links, track performance, and codify targeting parameters.

3.  **Marketing Teams**: Groups of marketing professionals working collaboratively on campaigns who need a centralized platform to coordinate efforts, share campaign information, and maintain consistency in tracking and attribution.

### Audience characteristics

1.  **Technical proficiency**: Moderate to high familiarity with digital marketing tools, UTM parameters, and campaign targeting concepts.
2.  **Organization size**: Small to medium-sized businesses (SMBs) and marketing agencies with teams of 2-10 marketers.
3.  **Pain points**:
    *   Managing campaign information across disparate spreadsheets and documents.
    *   Ensuring consistent UTM parameter usage for proper attribution.
    *   Coordinating targeting parameters among team members and across platforms.
    *   Lacking a central repository for campaign history and metadata.
4.  **Goals**:
    *   Improve campaign organization and documentation.
    *   Streamline the workflow for campaign setup and link generation.
    *   Enhance collaboration and knowledge sharing among team members.
    *   Increase campaign effectiveness through better-defined targeting.

## Features and requirements

### 1. Authentication and User Management

#### 1.1 Login / Signup
-   User authentication via Google OAuth and Email/Password.
-   Role-based access control (Manager vs. Team Member).
-   Domain registration for identifying an organization.
-   Team member invitation system via email per domain

#### 1.2 User Roles and Permissions
-   **Manager**: Full access to the domain. Can manage subscriptions, add/remove team members, manage all campaigns and links within the domain.
-   **Team Member**: Can create and manage their own campaigns and links. Can view all campaigns and links created by other members within the same domain.

### 2. Campaign Management

#### 2.1 Campaign Creation
-   Form-based campaign setup with fields for name, objective, etc.
-   Audience and interest definition fields.
-   Hierarchical targeting criteria selection (e.g., Geo > Country > State).
-   Automatic generation of a unique and readable campaign ID.
-   Centralized dashboard to view all created and stored campaigns.

#### 2.2 Campaign Metadata Management
-   Full editing capabilities for existing campaigns (permission-based).
-   Campaign visibility across all team members in the domain.
-   Export campaign data to CSV.

### 3. URL and UTM Management

#### 3.1 Link Generation
-   UTM parameter configuration form (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`).
-   UTM Source(`utm_source`) is any one of the marketing vendors which will be used for campaign distribution
-   Automatic pre-filling of `utm_campaign` based on the parent campaign.
-   Standardization rules and validation for UTM parameters.
-   Creation and storage of UTM links, associated with a parent campaign.

#### 3.2 Link Management
-   Edit existing UTM links.
-   Group and view links by their parent campaign.
-   Bulk operations for link management (e.g., archive, delete).

### 4. Reporting and Analytics

#### 4.1 Campaign Performance Tracking
-   ***[Note for V1 Scope]:*** *Initial reporting will focus on data generated within Utmato (e.g., number of links created per campaign, campaign status tracking).*
-   ***[Future Scope - V2]:*** *Integration with marketing platforms (e.g., Google Ads, Facebook Ads) for data retrieval of impressions, clicks, conversions, spend, and ROI.*
-    ***[Future Scope - V2]:*** *Dashboard widgets to visualize campaign activity.*
-   Export capabilities for all reports.

### 5. Landing Page and Marketing Site

#### 5.1 Public-Facing Website
-   Modern, conversion-optimized landing page.
-   Clear presentation of features, benefits, and pricing.
-   Call-to-action for a free trial.
-   Links for login and signup.

### 6. Subscription and Billing

#### 6.1 Subscription Management
-   Free 7-day trial for new domains, no credit card required.
-   Monthly subscription option: $7.99/month per domain.
-   Annual subscription option: $5.99/month per domain (billed annually).
-   Stripe integration for secure payment processing.
-   Domain-based subscription model.
-   User limit enforcement (10 users maximum per domain).

## User stories and acceptance criteria

### Authentication and User Management

#### ST-101: User registration as a Marketing Manager
**As a** marketing professional,
**I want to** register a new account and a new domain on Utmato,
**So that** I can start setting up my organization and managing campaigns.

**Acceptance Criteria:**
1.  A user can sign up using Google OAuth or an email and password.
2.  During registration, the user must provide a domain name (e.g., `mycompany.com`) to create their organization.
3.  Upon successful registration, the user is assigned the **Manager** role for that domain.
4.  The user is redirected to the main dashboard after registration.
5.  A welcome email is sent to the user with instructions for getting started.

#### ST-103: Manager inviting team members
**As a** marketing manager,
**I want to** invite team members to join my domain on Utmato,
**So that** we can collaborate on campaign management.

**Acceptance Criteria:**
1.  The Manager can access an "Invite Team" or "User Management" section.
2.  The Manager can input one or more email addresses to send invitations.
3.  The system sends an invitation email with a unique registration link to each address.
4.  The Manager can view the status of invitations (Pending, Accepted).
5.  The system enforces the 10-user limit per domain, preventing further invitations if the limit is reached.

#### ST-104: Manager managing team members
**As a** marketing manager,
**I want to** view a list of all team members and remove them if necessary,
**So that** I can maintain an up-to-date and secure list of users with access to my organization's data.

**Acceptance Criteria:**
1.  A Manager can access a "User Management" or "Team" page.
2.  The page lists all current members of the organization, showing their email and role.
3.  A Manager can click a "Remove" button next to a team member's name.
4.  The system asks for confirmation before removing the user.
5.  Upon removal, the user can no longer access the organization's data, and the user count is updated.
6.  A Manager cannot remove themselves.

### Campaign Management

#### ST-201: Creating a new campaign
**As a** marketing team member,
**I want to** create a new marketing campaign with standardized parameters,
**So that** I can organize my marketing efforts and ensure consistent tracking.

**Acceptance Criteria:**
1.  The user can access a "Create Campaign" form from the dashboard.
2.  The form requires a campaign name, objective.
3.  The user can optionally add details for audiences, deomgraphics, targeting, interests, and notes.
4.  Upon saving, the system generates a unique, human-readable Campaign ID.
5.  The new campaign appears on the main campaign dashboard.

#### ST-203: Editing campaign metadata
**As a** marketing manager,
**I want to** edit any campaign's metadata within my domain,
**So that** I can update information or correct errors made by my team.

**Acceptance Criteria:**
1.  A user with the **Manager** role can select "Edit" for any campaign in the domain.
2.  A user with the **Team Member** role can only edit campaigns they created.
3.  The edit form is pre-populated with the existing campaign data.
4.  All changes are validated and saved.
5.  An activity log tracks significant changes to a campaign (e.g., who made the edit and when).

### URL and UTM Management

#### ST-301: Generating campaign links
**As a** marketing team member,
**I want to** generate a tracked URL with correct UTM parameters for a campaign,
**So that** I can accurately track its performance in our analytics tools.

**Acceptance Criteria:**
1.  Within a campaign's detail view, the user can access a "Generate Link" function.
2.  The `utm_campaign` fields are pre-filled from the parent campaign data. `utm_source` is based on a several marketing vendor options like facebook , tiktok etc; it is an exhasutinve list of 100 sources. 
3.  The user must provide a destination URL and `utm_medium`. Sometimes it is also known as adgroup
4.  `utm_content` and `utm_term` are optional.Sometimes `utm_content` also refers to creative identifier or a ad level identifier
5.  The system generates and displays the full, URL-encoded link.
6.  The generated link is saved and listed under the parent campaign.
7.  A "Copy to Clipboard" button is provided for the generated link.


## Technical Epics / Non-Functional Requirements

*(These are developer-focused tasks essential for the product's foundation)*

#### TE-601: Database Schema Implementation
**As a** backend developer,
**I want to** implement a robust and scalable database schema,
**So that** all application data is stored efficiently, securely, and with relational integrity.

**Acceptance Criteria:**
1.  Schema includes tables for `organizations`, `users`, `roles`, `campaigns`, `links`, and `subscriptions`.
2.  Proper foreign key constraints are used to link tables (e.g., links to campaigns, users to organizations).
3.  Appropriate indexes are created on frequently queried columns (e.g., `user_id`, `organization_id`, `campaign_id`).
4.  Audit fields (`created_at`, `updated_at`, `created_by`) are included in key tables.
5.  Data validation rules (e.g., NOT NULL constraints) are enforced at the database level.

#### TE-602: Database Backup and Recovery
**As a** system administrator,
**I want to** implement automated database backup and recovery procedures,
**So that** user data is protected against accidental loss or corruption.

**Acceptance Criteria:**
1.  Automated daily backups are configured for the production database.
2.  Point-in-Time Recovery (PITR) is enabled for at least 7 days.
3.  The recovery process is documented and has been tested at least once.
4.  Monitoring and alerts are configured to report backup failures.

#### TE-603: Error Tracking and Monitoring Implementation
**As a** developer,
**I want to** integrate a comprehensive error tracking tool like Sentry,
**So that** we can proactively identify, diagnose, and resolve issues in production.

**Acceptance Criteria:**
1.  Sentry SDK is integrated into the Next.js frontend and the FastAPI backend.
2.  Source maps are uploaded during the CI/CD deployment process to de-minify stack traces.
3.  User context (ID, email) is attached to error reports for easier debugging.
4.  Performance monitoring (APM) is enabled for key API endpoints and frontend transactions.
5.  Alerting rules are configured to notify the development team of critical errors via Slack/email.

## Technical requirements / stack

### Frontend
-   **Framework**: **Next.js** (React)
-   **Styling**: **Tailwind CSS** with **shadcn/ui** component library.
-   **State Management**: React Context/Zustand as needed.
-   **Hosting**: **Vercel**

### Backend
-   **Framework**: **Python 3.10+** with **FastAPI**.
-   **Key Libraries**:
    -   `Pydantic` for data validation and settings management.
    -   `SQLAlchemy 2.0` (async) or `SQLModel` for the ORM.
    -   `Alembic` for database migrations.
-   **Hosting**: Containerized deployment on a service like **Render**, **Fly.io**, or **AWS ECS**.

### API Design
-   **Architecture**: RESTful principles.
-   **Documentation**: FastAPI will automatically generate **OpenAPI (Swagger UI)** and **ReDoc** documentation for all endpoints.
-   **Endpoints**:

| Method | Endpoint | Description | Role Required |
| :--- | :--- | :--- |:--- |
| POST | `/api/v1/invitations` | Sends an invitation to a new team member. | Manager |
| GET | `/api/v1/campaigns` | Lists all campaigns for the user's organization. | Team Member |
| POST | `/api/v1/campaigns` | Creates a new campaign. | Team Member |
| GET | `/api/v1/campaigns/{campaign_id}` | Retrieves a single campaign by its ID. | Team Member |
| PUT | `/api/v1/campaigns/{campaign_id}` | Updates an existing campaign. | Team Member |
| DELETE | `/api/v1/campaigns/{campaign_id}` | Deletes a campaign. | Manager |
| GET | `/api/v1/campaigns/{campaign_id}/links` | Lists all UTM links associated with a campaign. | Team Member |
| POST | `/api/v1/campaigns/{campaign_id}/links` | Creates a new UTM link for a campaign. | Team Member |
| PUT | `/api/v1/links/{link_id}` | Updates an existing UTM link. | Team Member |
| DELETE | `/api/v1/links/{link_id}` | Deletes a UTM link. | Team Member |
| GET | `/api/v1/users/me` | Retrieves the profile of the current user. | Team Member |
| GET | `/api/v1/organization` | Retrieves the details of the user's organization. | Team Member |
| PUT | `/api/v1/organization` | Updates organization details. | Manager |
| **GET** | **`/api/v1/organization/users`** | **Lists all users within the current user's organization.** | **Manager** |
| **DELETE** | **`/api/v1/organization/users/{user_id}`** | **Removes a user from the organization.** | **Manager** |
| POST | `/api/v1/billing/create-checkout-session`| Initiates a Stripe subscription checkout. | Manager |
| GET | `/api/v1/billing/portal` | Redirects a user to their Stripe billing portal. | Manager |

-   **Authentication**: Endpoints will be protected and expect a JWT issued by Clerk. The backend will validate the token on every request.

-   **Authentication**: Endpoints will be protected and expect a JWT issued by Clerk. The backend will validate the token on every request.

### Database
-   **Service**: **Supabase** (PostgreSQL).
-   **Schema Definition**:
```sql
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
```
-   **Usage**: Utmato will use Supabase primarily as a hosted PostgreSQL database. Its built-in API and auth features will not be the primary interface for the application logic, which resides in the FastAPI backend.

### Authentication
-   **Service**: **Clerk**.
-   **Integration**:
    -   **Frontend**: Clerk's React components will be used for sign-in, sign-up, and user profile management UI.
    -   **Backend**: The FastAPI backend will use Clerk's libraries to validate the JWT sent in the `Authorization` header of incoming requests.

### DevOps and Tooling
-   **Source Control**: **Git** with a **GitHub** monorepo (or separate frontend/backend repos).
-   **Monorepo Structure**: Frontend and backend components reside in a single repository for streamlined development and dependency management.
-   **CI/CD**: **GitHub Actions** for automated testing, building container images, and deploying to hosting services.
-   **Error Tracking**: **Sentry** for both frontend and backend.
-   **Session Replay**: **LogRocket** (Optional, for advanced frontend debugging).

### Infrastructure Requirements
-   **Security**:
    -   HTTPS on all connections.
    -   Data encryption at rest (provided by Supabase) and in transit.
    -   Input validation on all API endpoints (handled by FastAPI/Pydantic).
    -   Protection against common web vulnerabilities (XSS, CSRF).
-   **Performance**:
    -   API response time < 300ms for 95% of requests.
    -   Page load time (LCP) < 2.5 seconds.
    -   99.9% uptime guarantee.

## Design and user interface

### General Design Principles
1.  **Clean and Professional**: A modern, minimal design that emphasizes organization and efficiency.
2.  **Intuitive Navigation**: A clear information hierarchy with logical grouping of related functions.
3.  **Responsive Design**: Fully functional and aesthetically pleasing across desktop, tablet, and mobile devices.
4.  **Consistent Styling**: A uniform color scheme, typography, and component design language throughout the application.
5.  **Accessibility**: Strive for WCAG 2.1 AA compliance.

### Key Interface Components
-   **Dashboard**: Main landing page after login, showing summary statistics, recent campaigns, and quick-action buttons.
-   **Campaign Management View**: A filterable and searchable table/list of all campaigns, showing key details like name, ID, status, and creation date.
-   **Campaign Detail View**: A dedicated page for a single campaign, showing all of its metadata, notes, and a list of all associated UTM links.
-   **Creation/Editing Modals/Forms**: Intuitive forms for creating/editing campaigns and links, with clear validation feedback.
-   **User/Domain Management Settings**: A dedicated area for Managers to handle billing, invite users, and manage domain settings.