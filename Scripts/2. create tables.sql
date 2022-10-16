create table users (
	id serial primary key,
	userName varchar(50),
	mail varchar(100),
	password varchar(100)
);


create table tasks(
	id serial primary key,
	idUser BIGINT,
	fileName varchar(500),
	fileLocation varchar(500),
	status varchar(30),
	originalFormat varchar(10),
	desiredFormat varchar(10),
	uploadedDatetime timestamp,
	processedDatetime timestamp,
	constraint fk_user
	  FOREIGN KEY(idUser) 
	  REFERENCES users(id)
);
