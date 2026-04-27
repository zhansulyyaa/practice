-- Adds a phone number to an existing contact by name
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    -- Find the contact
    SELECT id INTO v_id FROM contacts WHERE username = p_contact_name;
    IF v_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    RAISE NOTICE 'Phone added to "%".', p_contact_name;
END;
$$;


-- Moves a contact to a group; creates the group if it doesn't exist
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id   INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Create group if missing
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;

    -- Find contact
    SELECT id INTO v_contact_id FROM contacts WHERE username = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    RAISE NOTICE 'Moved "%" to group "%".', p_contact_name, p_group_name;
END;
$$;


-- Searches contacts by name, email, or any of their phone numbers
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    id       INTEGER,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name AS grp
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE
        c.username ILIKE '%' || p_query || '%'
        OR c.email  ILIKE '%' || p_query || '%'
        OR p.phone  ILIKE '%' || p_query || '%';
END;
$$;


-- Paginated listing of contacts (reused from Practice 8 style)
CREATE OR REPLACE FUNCTION paginate_contacts(p_limit INT, p_offset INT)
RETURNS TABLE (
    id       INTEGER,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name AS grp
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.username
    LIMIT p_limit OFFSET p_offset;
END;
$$;
