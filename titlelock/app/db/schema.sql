-- DeedGuard USA — data model (Postgres / Supabase)
-- Run this in the Supabase SQL editor (or psql) to create the schema.

create extension if not exists "pgcrypto";

-- Free-check leads (top of funnel)
create table if not exists leads (
  id          uuid primary key default gen_random_uuid(),
  email       text not null,
  address     text not null,
  source      text default 'free-check',
  status      text default 'new',          -- new | contacted | converted | dead
  created_at  timestamptz not null default now()
);

-- Paying subscribers (source of truth synced from Stripe)
create table if not exists subscribers (
  id                      uuid primary key default gen_random_uuid(),
  email                   text unique not null,
  stripe_customer_id      text unique,
  stripe_subscription_id  text,
  plan                    text,            -- essential | defend | premier
  status                  text default 'active',  -- active | past_due | canceled
  created_at              timestamptz not null default now()
);

-- Properties under watch (one subscriber may have several)
create table if not exists properties (
  id              uuid primary key default gen_random_uuid(),
  subscriber_id   uuid references subscribers(id) on delete cascade,
  address         text not null,
  county          text,
  state           text default 'FL',
  parcel_id       text,
  owner_name      text,
  baseline        jsonb,                   -- known-good recordings snapshot
  last_scanned_at timestamptz,
  created_at      timestamptz not null default now()
);

-- Every scan we run (audit trail + change flag)
create table if not exists scans (
  id           uuid primary key default gen_random_uuid(),
  property_id  uuid references properties(id) on delete cascade,
  scanned_at   timestamptz not null default now(),
  records      jsonb,                      -- recordings seen this scan
  changed      boolean default false
);

-- Alerts raised when something new is detected
create table if not exists alerts (
  id           uuid primary key default gen_random_uuid(),
  property_id  uuid references properties(id) on delete cascade,
  severity     text,                        -- info | warning | critical
  kind         text,                        -- deed | mortgage | lien | judgment | other
  summary      text,
  record       jsonb,
  notified     boolean default false,
  created_at   timestamptz not null default now()
);

create index if not exists idx_properties_subscriber on properties(subscriber_id);
create index if not exists idx_scans_property on scans(property_id);
create index if not exists idx_alerts_property on alerts(property_id);
