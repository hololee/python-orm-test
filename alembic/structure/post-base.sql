
CREATE TABLE users (
	id SERIAL NOT NULL, 
	name VARCHAR, 
	age INTEGER, 
	sex INTEGER, 
	CONSTRAINT users_pkey PRIMARY KEY (id)
);
