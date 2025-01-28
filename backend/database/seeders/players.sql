INSERT INTO players (name, email, gdpr_consent) VALUES
    ('Mikko Korhonen', 'mikko.korhonen@gmail.com', true),
    ('Anna Virtanen', 'anna.virtanen@outlook.com', true),
    ('Pekka Mäkinen', 'pekka.makinen@gmail.com', true),
    ('Laura Nieminen', 'laura.nieminen@hotmail.com', true),
    ('Jukka Hämäläinen', 'jukka.hamalainen@gmail.com', true),
    ('Sari Laine', 'sari.laine@outlook.com', true),
    ('Antti Lehtonen', 'antti.lehtonen@gmail.com', true),
    ('Tiina Salminen', 'tiina.salminen@hotmail.com', true),
    ('Matti Järvinen', 'matti.jarvinen@gmail.com', true),
    ('Hanna Koskinen', 'hanna.koskinen@outlook.com', true),
    ('Jouni Heiskanen', 'jouni.heiskanen@gmail.com', true),
    ('Katja Leinonen', 'katja.leinonen@outlook.com', true),
    ('Marko Kinnunen', 'marko.kinnunen@gmail.com', true),
    ('Elina Rantanen', 'elina.rantanen@hotmail.com', true),
    ('Tero Lahtinen', 'tero.lahtinen@gmail.com', true)
ON CONFLICT (email) DO NOTHING;
