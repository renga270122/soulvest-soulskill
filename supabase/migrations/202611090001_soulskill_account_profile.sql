-- SoulSkill account and candidate profile foundation.
-- Apply with: supabase db push (after linking the intended Supabase project).

create extension if not exists pgcrypto;

create table if not exists public.workspaces (
    id uuid primary key default gen_random_uuid(),
    owner_user_id uuid not null references auth.users(id) on delete cascade,
    name text not null default 'Personal workspace',
    workspace_type text not null default 'personal'
        check (workspace_type in ('personal', 'organization')),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique (owner_user_id, workspace_type)
);

create table if not exists public.workspace_members (
    workspace_id uuid not null references public.workspaces(id) on delete cascade,
    user_id uuid not null references auth.users(id) on delete cascade,
    role text not null default 'owner'
        check (role in ('owner', 'admin', 'member')),
    created_at timestamptz not null default now(),
    primary key (workspace_id, user_id)
);

create table if not exists public.candidate_profiles (
    user_id uuid primary key references auth.users(id) on delete cascade,
    full_name text not null default '',
    career_stage text not null default 'exploring'
        check (career_stage in ('fresher', 'career_restart', 'career_growth', 'exploring')),
    current_title text not null default '',
    headline text not null default '',
    summary text not null default '',
    years_experience numeric(4,1) not null default 0
        check (years_experience >= 0 and years_experience <= 60),
    target_roles text[] not null default '{}',
    target_locations text[] not null default '{}',
    country_code char(2) not null default 'IN',
    locale text not null default 'en-IN',
    timezone text not null default 'Asia/Kolkata',
    onboarding_completed_at timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists workspaces_owner_user_id_idx
    on public.workspaces(owner_user_id);
create index if not exists workspace_members_user_id_idx
    on public.workspace_members(user_id);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = public
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

drop trigger if exists workspaces_set_updated_at on public.workspaces;
create trigger workspaces_set_updated_at
before update on public.workspaces
for each row execute function public.set_updated_at();

drop trigger if exists candidate_profiles_set_updated_at on public.candidate_profiles;
create trigger candidate_profiles_set_updated_at
before update on public.candidate_profiles
for each row execute function public.set_updated_at();

-- Create a private personal workspace and profile for each new Supabase Auth user.
create or replace function public.handle_new_soulskill_user()
returns trigger
language plpgsql
security definer
set search_path = public, auth
as $$
declare
    new_workspace_id uuid;
    display_name text;
begin
    display_name := coalesce(
        nullif(trim(new.raw_user_meta_data ->> 'full_name'), ''),
        nullif(trim(new.raw_user_meta_data ->> 'name'), ''),
        ''
    );

    insert into public.workspaces (owner_user_id, name, workspace_type)
    values (new.id, 'Personal workspace', 'personal')
    on conflict (owner_user_id, workspace_type) do update
      set owner_user_id = excluded.owner_user_id
    returning id into new_workspace_id;

    insert into public.workspace_members (workspace_id, user_id, role)
    values (new_workspace_id, new.id, 'owner')
    on conflict (workspace_id, user_id) do nothing;

    insert into public.candidate_profiles (user_id, full_name)
    values (new.id, display_name)
    on conflict (user_id) do nothing;

    return new;
end;
$$;

drop trigger if exists on_auth_user_created_soulskill on auth.users;
create trigger on_auth_user_created_soulskill
after insert on auth.users
for each row execute procedure public.handle_new_soulskill_user();

alter table public.workspaces enable row level security;
alter table public.workspace_members enable row level security;
alter table public.candidate_profiles enable row level security;

revoke all on public.workspaces from anon;
revoke all on public.workspace_members from anon;
revoke all on public.candidate_profiles from anon;

grant select, update on public.workspaces to authenticated;
grant select on public.workspace_members to authenticated;
grant select, insert, update, delete on public.candidate_profiles to authenticated;

drop policy if exists "owners can read their personal workspaces" on public.workspaces;
create policy "owners can read their personal workspaces"
on public.workspaces for select to authenticated
using (owner_user_id = (select auth.uid()));

drop policy if exists "owners can update their personal workspaces" on public.workspaces;
create policy "owners can update their personal workspaces"
on public.workspaces for update to authenticated
using (owner_user_id = (select auth.uid()))
with check (owner_user_id = (select auth.uid()));

drop policy if exists "members can read their own memberships" on public.workspace_members;
create policy "members can read their own memberships"
on public.workspace_members for select to authenticated
using (user_id = (select auth.uid()));

drop policy if exists "users can read their own candidate profile" on public.candidate_profiles;
create policy "users can read their own candidate profile"
on public.candidate_profiles for select to authenticated
using ((select auth.uid()) is not null and user_id = (select auth.uid()));

drop policy if exists "users can insert their own candidate profile" on public.candidate_profiles;
create policy "users can insert their own candidate profile"
on public.candidate_profiles for insert to authenticated
with check ((select auth.uid()) is not null and user_id = (select auth.uid()));

drop policy if exists "users can update their own candidate profile" on public.candidate_profiles;
create policy "users can update their own candidate profile"
on public.candidate_profiles for update to authenticated
using ((select auth.uid()) is not null and user_id = (select auth.uid()))
with check ((select auth.uid()) is not null and user_id = (select auth.uid()));

drop policy if exists "users can delete their own candidate profile" on public.candidate_profiles;
create policy "users can delete their own candidate profile"
on public.candidate_profiles for delete to authenticated
using ((select auth.uid()) is not null and user_id = (select auth.uid()));
