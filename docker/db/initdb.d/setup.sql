CREATE TABLE Shops(
  shop_id       SERIAL PRIMARY KEY,
  shop_name      VARCHAR(40) NOT NULL,
  review_point   Decimal,
  geo_lat        Decimal,
  geo_lng        Decimal
);

CREATE TYPE day_enum AS ENUM ('月','火','水','木','金','土','日');

CREATE TABLE Shop_Time(
  id             SERIAL PRIMARY KEY,
  shop_id        INTEGER REFERENCES Shops(shop_id),
  sales_day      day_enum NOT NULL,
  start_time     Time NOT NULL,
  end_time       Time NOT NULL
);
