-- Extensions
create extension if not exists "pgcrypto";
create extension if not exists "vector";

-- Users table
create table if not exists users (
    id text primary key,
    name text not null,
    email text unique,
    created_at timestamptz default now()
);

-- Documents for RAG
create table if not exists documents (
    id uuid primary key default gen_random_uuid(),
    content text not null,
    metadata jsonb default '{}'::jsonb,
    embedding vector(384) not null,
    created_at timestamptz default now()
);

-- Agent sessions and memory
create table if not exists agent_sessions (
    id uuid primary key default gen_random_uuid(),
    user_id text,
    created_at timestamptz default now()
);

create table if not exists agent_messages (
    id uuid primary key default gen_random_uuid(),
    session_id uuid not null references agent_sessions(id) on delete cascade,
    role text not null,
    content text not null,
    created_at timestamptz default now()
);

-- Business events
create table if not exists events (
    id uuid primary key default gen_random_uuid(),
    event_type text not null,
    payload jsonb default '{}'::jsonb,
    created_at timestamptz default now()
);

-- Tickets (business example)
create table if not exists tickets (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    status text not null default 'open',
    priority text not null default 'medium',
    user_id text,
    context jsonb default '{}'::jsonb,
    created_at timestamptz default now()
);

-- Vector index
create index if not exists documents_embedding_idx
    on documents
    using ivfflat (embedding vector_cosine_ops)
    with (lists = 100);
