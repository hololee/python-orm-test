
CREATE TABLE users (
	id SERIAL NOT NULL, 
	name VARCHAR, 
	age INTEGER, 
	sex INTEGER, 
	region VARCHAR, 
	CONSTRAINT users_pkey PRIMARY KEY (id)
)



CREATE TABLE buckets (
	id SERIAL NOT NULL, 
	user_id INTEGER NOT NULL, 
	name VARCHAR, 
	mount INTEGER, 
	CONSTRAINT buckets_pkey PRIMARY KEY (id), 
	CONSTRAINT users_bucket_fk FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
)


