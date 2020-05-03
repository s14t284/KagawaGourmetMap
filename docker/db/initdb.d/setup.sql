CREATE TABLE Shops(
  shop_id        PRIMARY KEY,
  shop_name      VARCHAR(40),
);

CREATE TABLE Shop_Time(
  sales_day      VARCHAR(40),
  start_time     Time,
  end_time       Time,
  foreign key(shop_id) references Shops(shop_id)
);

CREATE TABLE Shop_Point(
  shop_point      Decimal,
  foreign key(shop_id) references Shops(shop_id)
);

CREATE TABLE Shop_Geo(
  geo_lat      Decimal,
  get_lng      Decimal,
  foreign key(shop_id) references Shops(shop_id)
);

