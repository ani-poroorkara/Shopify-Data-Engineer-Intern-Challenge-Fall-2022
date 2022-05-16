DROP TABLE IF EXISTS image_information;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS login_info;

CREATE TABLE users
( 
    user_id TEXT PRIMARY KEY,
	email TEXT NOT NULL UNIQUE,
	fname TEXT NOT NULL,
	pass PASSWORD NOT NULL,
	phone TEXT NOT NULL UNIQUE
);

CREATE TABLE login_info
( 
	email TEXT PRIMARY KEY,
	pass PASSWORD
);

CREATE TABLE image_information
( 
    id INTEGER PRIMARY KEY,
    seller TEXT,
    img_name TEXT,
    img BLOB NOT NULL, 
    discount INTEGER,
    price INTEGER NOT NULL,
    FOREIGN KEY(seller) REFERENCES users(user_id)
);