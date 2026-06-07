INSERT INTO teams (id, name, slug) VALUES
('00000000-0000-0000-0000-000000000001', 'Acme Cloud Platform', 'acme')
ON CONFLICT (id) DO NOTHING;

INSERT INTO services (id, team_id, name, environment, description, repository_url, healthcheck_url, metadata) VALUES
('00000000-0000-0000-0000-000000000003', '00000000-0000-0000-0000-000000000001', 'payments-api', 'production', 'Handles checkout payment authorization and capture.', 'https://github.com/acme/payments-api', 'https://payments.acme.dev/health', '{"owner":"platform-team","current_version":"v42"}')
ON CONFLICT (id) DO NOTHING;
