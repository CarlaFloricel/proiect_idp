CREATE TABLE movies (
  movieId VARCHAR(20),
  name VARCHAR(50),
  displayDay INT,
  displayHour INT,
  numberOfSeats INT
);


CREATE TABLE reservedSeats (
	movieId VARCHAR(20),
	numberOfSeats INT,
    reservationId INT

);

