package handler

import (
	"net/http"
	"github.com/labstack/echo"
	//"github.com/coopernurse/gorp"
	"database/sql"
	_ "github.com/lib/pq"
	"github.com/pkg/errors"
	"time"
	"strconv"
)

var Db *sql.DB

func init() {
	var err error
	// 後でDB情報は変更
	Db, err = sql.Open("postgres", "host=localhost port=5432 user=postgres password=Passw0rd dbname=test1 sslmode=disable")
    if err != nil {
        panic(err)
    }
}

type Shop struct {
    ID int `json:"id"`
	Name string `json:"shop_name"`
	Times Time
	Point float64 `json:"review_point"`
	Geos Geo
}

type Time struct {
	Day string `json:"day"`
	StartTime time.Time `json:"starttime"`
	EndTime time.Time `json:"endtime"`
}

type Geo struct {
    Latitude float64 `json:"lat"`
    Longitude float64 `json:"lng"`
}

/*
func GetShops() echo.HandlerFunc {
	return func(c echo.Context) error {
		shopname := c.QueryParams("shop_name")
		shop := Shop{}
		shops := []*Shop{}
		geo := Geo{}
		timesinfo := Time{}

		if shopname == "" {
			data, err := Db.Query("select * from shops")
		}
		// クエリありの場合を追加する

		if err != nil {
			return errors.Wrapf(err, "connot connect SQL")
		}
		defer data.Close()

		for data.Next(){
			if err := data.Scan(&shop.Id, &shop.Name, &shop.Point,&geo.Latitude,&geo.Longitude); err != nil {
				return errors.Wrapf(err, "connot connect SQL")
			}
			if err1 := Db.Query("select sales_day,start_time,end_time from Shop_Time where shop_id = $1",shopid).Scan(&timesinfo.Day,&timesinfo.StartTime,&timesinfo.EndTime); err1 != nil {
				return errors.Wraf(err1, "connot connect SQL")
			}	
			shops = append(shops, &Shop{Id: shop.Id, Name: shop.Name,Times: {timesinfo.Day,timesinfo.StartTime,timesinfo.EndTime}, Point: shop.Point, Geo: {geo.Latitude,geo.Longitude}})
		}
        return c.JSON(http.StatusOK, shops)
	}
}
*/
func GetShop() echo.HandlerFunc {
	return func(c echo.Context) error {
		id,_ := strconv.Atoi(c.Param("id"))
		shop := Shop{}
		shops := []*Shop{}
		geo := Geo{}
		timesinfo := Time{}

		if err := Db.QueryRow("select * from Shops where shop_id = $1",&id).Scan(&shop.ID, &shop.Name, &shop.Point, &geo.Latitude, &geo.Longitude); err != nil {
			return errors.Wrapf(err, "connot connect SQL")
		}
		if err1 := Db.QueryRow("select sales_day,start_time,end_time from Shop_Time where shop_id = $1",id).Scan(&timesinfo.Day,&timesinfo.StartTime,&timesinfo.EndTime); err1 != nil {
			return errors.Wrapf(err1, "connot connect SQL")
		}
		shops = append(shops,&Shop{ID: shop.ID,Name: shop.Name,Times: timesinfo,Point: shop.Point,Geos: geo})
        return c.JSON(http.StatusOK, shops)
	}
}

func Gettest() echo.HandlerFunc {
	return func(c echo.Context) error {
		//ids := c.Param("id")
		//id,_ := strconv.Atoi(ids)
		//var test string
		//Db.QueryRow("select shop_name from Shops where shop_id = $1",id).Scan(&test)
		_,err := Db.Query("select * from Shops;")
		return c.JSON(http.StatusOK,err)
	}
}

/* 
// レビューを登録(sqlを作成してから)
func PostReview() echo.HandlerFunc {
	return func(c echo.Context) error {

	}
}*/