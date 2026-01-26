CREATE TABLE IF NOT EXISTS malicious_urls (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL
);

INSERT INTO malicious_urls (url)
VALUES
    ('www.bad.com/malware'),
    ('evil.com/phishing'),
    ('malware.test/download'),
    ('17ebook.com'),
    ('aladel.net'),
    ('clicnews.com'),
    ('fantasticfilms.ru')
ON CONFLICT DO NOTHING;
