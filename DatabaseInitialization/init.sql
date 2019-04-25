CREATE TABLE movies (
  movieId VARCHAR(20),
  name VARCHAR(50),
  displayDay INT,
  displayHour INT
);

CREATE TABLE seats (
	movieId VARCHAR(20),
	numberOfSeats INT,
	reservedSeats INT,
	boughtSeats INT
);

