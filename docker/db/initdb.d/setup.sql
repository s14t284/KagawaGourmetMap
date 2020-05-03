CREATE TABLE Shops(
  shop_id        PRIMARY KEY,
  shop_name      VARCHAR(40),
  review_point   Decimal,
  geom           geography(POINT,4326) NOT NULL
);

CREATE TYPE day_enum AS ENUM ('月','火','水','木','金','土','日');

CREATE TABLE Shop_Time(
  sales_day      day_enum,
  start_time     Time NOT NULL,
  end_time       Time NOT NULL,
  foreign key(shop_id) references Shops(shop_id)
);
