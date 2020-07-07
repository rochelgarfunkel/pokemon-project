USE pokemon;

CREATE TABLE owners(
    name VARCHAR(20) NOT NULL PRIMARY KEY,
    town VARCHAR(20)
);


CREATE TABLE pokemon(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(20),
    height INT,
    weight INT
);

CREATE TABLE pokemon_owners(
    owner_name VARCHAR(20),
    pokemon_id INT,
    PRIMARY KEY(owner_name, pokemon_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
    FOREIGN KEY(owner_name) REFERENCES owners(name)
);

CREATE TABLE pokemon_types(
    pokemon_id INT,
    type VARCHAR(20),
    PRIMARY KEY(pokemon_id, type),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
);

-- DROP TABLE pokemon_owners;
-- DROP TABLE pokemon;
-- DROP TABLE owners;
-- DROP DATABASE pokemon;
-- CREATE DATABASE pokemon;

