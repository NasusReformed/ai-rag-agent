insert into users (id, name, email) values
('u_1001', 'Ana Morales', 'ana@example.com'),
('u_1002', 'Luis Paredes', 'luis@example.com')
on conflict do nothing;

-- Example knowledge base docs
-- Use the embeddings endpoint to index these docs; this seed only provides text examples.
