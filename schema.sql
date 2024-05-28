CREATE TABLE IF NOT EXISTS manager (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    company TEXT NOT NULL,
    industry TEXT NOT NULL,
    is_manager INTEGER NOT NULL DEFAULT 0,
    creation TIMESTAMP NOT NULL,
    account_type INTEGER NOT NULL DEFAULT 1
);