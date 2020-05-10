import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import pdb


class Tabelog:
    def __init__(
        self, base_url, test_mode=False, p_ward="香川県", begin_page=1, end_page=12
    ):

        # 変数宣言
        self.store_id = ""
        self.store_id_num = 0
        self.store_name = ""
        self.score = 0
        self.ward = p_ward
        self.review_cnt = 0
        self.review = ""
        self.columns = [
            "store_id",
            "store_name",
            "jenre",
            "shop_url",
            "cake_image",
            "score",
            "open_hours",
            "rest_time",
            "budget_lunch",
            "budget_dinner",
            "address",
            "review",
        ]
        self.df = pd.DataFrame(columns=self.columns)
        self.__regexcomp = re.compile(r"\n|\s")  # \nは改行、\sは空白

        page_num = begin_page  # 店舗一覧ページ番号

        if test_mode:
            list_url = (
                base_url + str(page_num) + "/?Srt=D&SrtT=rt&sort_mode=1"
            )  # 食べログの点数ランキングでソートする際に必要な処理
            self.scrape_list(list_url, mode=test_mode)
        else:
            while True:
                list_url = (
                    base_url + str(page_num) + "/?Srt=D&SrtT=rt&sort_mode=1"
                )  # 食べログの点数ランキングでソートする際に必要な処理
                if self.scrape_list(list_url, mode=test_mode) != True:
                    break

                # INパラメータまでのページ数データを取得する
                if page_num >= end_page:
                    break
                page_num += 1
        return

    def scrape_list(self, list_url, mode):
        """
        店舗一覧ページのパーシング
        """
        r = requests.get(list_url)
        time.sleep(3)
        if r.status_code != requests.codes.ok:
            return False

        soup = BeautifulSoup(r.content, "html.parser")
        soup_a_list = soup.find_all("a", class_="list-rst__rst-name-target")  # 店名一覧

        if len(soup_a_list) == 0:
            return False

        if mode:
            for soup_a in soup_a_list[:2]:
                item_url = soup_a.get("href")  # 店の個別ページURLを取得
                self.store_id_num += 1
                self.scrape_item(item_url, mode)
        else:
            for soup_a in soup_a_list:
                item_url = soup_a.get("href")  # 店の個別ページURLを取得
                self.store_id_num += 1
                self.scrape_item(item_url, mode)

        return True

    def scrape_item(self, item_url, mode):
        """
        個別店舗情報ページ
        """
        start = time.time()

        r = requests.get(item_url)
        time.sleep(3)
        if r.status_code != requests.codes.ok:
            print(f"error:not found{ item_url }")
            return

        soup = BeautifulSoup(r.content, "html.parser")

        # 店舗名称取得
        store_name_tag = soup.find("h2", class_="display-name")
        store_name = store_name_tag.span.string
        print("{}→店名：{}".format(self.store_id_num, store_name.strip()), end="")
        self.store_name = store_name.strip()

        # 店舗URL取得
        self.shop_url = item_url

        # ケーキ屋取得
        ## 複数のジャンルが存在、{ケーキ,カフェ}の形式で保持できるようにする
        """
        store_head = soup.find("div", class_="rdheader-subinfo")
        store_head_list = store_head.find_all("dl")
        store_head_list = store_head_list[1].find_all("span")
        if store_head_list[0].text not in {"ケーキ"}:
            print("対象外")
            self.store_id_num -= 1
            return
        """

        # 評価点数取得
        rating_score_tag = soup.find("b", class_="c-rating__val")
        rating_score = rating_score_tag.span.string
        print("  評価点数：{}点".format(rating_score), end="")
        self.score = rating_score

        # 評価点数が存在しない店舗は除外
        if rating_score == "-":
            print("  評価がないため処理対象外")
            self.store_id_num -= 1
            return
        """
        # 評価が3.5未満店舗は除外
        if float(rating_score) < 3.5:
            print('  食べログ評価が3.5未満のため処理対象外')
            self.store_id_num -= 1
            return
        """

        # 予算
        budget = soup.find("div", class_="rstinfo-table__budget")
        budget_lunch = budget.find("em", class_="gly-b-lunch")
        budget_dinner = budget.find("em", class_="gly-b-dinner")
        try:
            self.budget_lunch = budget_lunch.text
        except:
            self.budget_lunch = None
        try:
            self.budget_dinner = budget_dinner.text
        except:
            self.budget_dinner = None

        # 住所取得
        addresses = soup.find("p", class_="rstinfo-table__address")
        self.address = addresses.text

        # 営業時間取得
        item_table = soup.find_all(
            "table", class_="c-table c-table--form rstinfo-table__table"
        )
        item_jenre_list = item_table[0].find_all("p")
        openday_list = []
        open_flag = False
        rest_flag = False
        for item in item_jenre_list:
            if rest_flag == True:
                restday = item.text
                self.rest_time = restday
                break
            if open_flag == True:
                openday_list.append(item.text)
            if item.text in "営業時間":
                open_flag = True
            elif item.text in "定休日":
                rest_flag = True
                open_flag = False
        openday_list.pop(-1)
        self.open_hours = ",".join(openday_list)

        # ケーキ画像URL取得
        images = soup.find(class_="js-imagebox-trigger")
        self.cake_image = images.get("href")

        # ジャンル取得
        item_list = soup.find_all("dd", class_="rdheader-subinfo__item-text")
        item_jenre_list = item_list[1].find_all(class_="linktree__parent-target-text")
        jenre_list = []
        for jenre in item_jenre_list:
            jenre_list.append(jenre.text)
        self.jenre = ",".join(jenre_list)

        # レビュー一覧URL取得
        review_tag_id = soup.find("li", id="rdnavi-review")
        review_tag = review_tag_id.a.get("href")

        # レビュー件数取得
        print(
            "  レビュー件数：{}".format(
                review_tag_id.find("span", class_="rstdtl-navi__total-count").em.string
            ),
            end="",
        )
        self.review_cnt = review_tag_id.find(
            "span", class_="rstdtl-navi__total-count"
        ).em.string

        # レビュー一覧ページ番号
        page_num = 1  # 1ページ*20 = 20レビュー 。この数字を変えて取得するレビュー数を調整。

        while True:
            review_url = (
                review_tag + "COND-0/smp1/?lc=0&rvw_part=all&PG=" + str(page_num)
            )
            # print('\t口コミ一覧リンク：{}'.format(review_url))
            print(" . ", end="")  # LOG
            if self.scrape_review(review_url) != True:
                break
            if page_num >= 1:
                break
            page_num += 1

        process_time = time.time() - start
        print("  取得時間：{}".format(process_time))

        return

    def scrape_review(self, review_url):
        """
        レビュー一覧ページのパーシング
        """
        r = requests.get(review_url)
        time.sleep(3)
        if r.status_code != requests.codes.ok:
            print(f"error:not found{ review_url }")
            return False

        # 各個人の口コミページ詳細へのリンクを取得する
        soup = BeautifulSoup(r.content, "html.parser")
        review_url_list = soup.find_all("div", class_="rvw-item")  # 口コミ詳細ページURL一覧

        if len(review_url_list) == 0:
            return False

        for url in review_url_list:
            review_detail_url = "https://tabelog.com" + url.get("data-detail-url")
            # print('\t口コミURL：', review_detail_url)
            # 口コミのテキストを取得
            self.get_review_text(review_detail_url)

        return True

    def get_review_text(self, review_detail_url):
        """
        口コミ詳細ページをパーシング
        """
        r = requests.get(review_detail_url)
        time.sleep(3)
        if r.status_code != requests.codes.ok:
            print(f"error:not found{ review_detail_url }")
            return

        soup = BeautifulSoup(r.content, "html.parser")
        review = soup.find_all(
            "div", class_="rvw-item__rvw-comment"
        )  # reviewが含まれているタグの中身をすべて取得
        if len(review) == 0:
            review = ""
        else:
            review = str(review[0].find("p"))
            review = re.sub("\s+|\\n|<p>|</p>", "", review)
            review = re.sub("<br/>", " ", review)
            review = re.sub("\s+", " ", review)
        # print('\t\t口コミテキスト：', review)
        self.review = review

        # データフレームの生成
        self.make_df()
        return

    def make_df(self):
        self.store_id = str(self.store_id_num).zfill(8)  # 0パディング
        se = pd.Series(
            [
                self.store_id,
                self.store_name,
                self.jenre,
                self.shop_url,
                self.cake_image,
                self.score,
                self.open_hours,
                self.rest_time,
                self.budget_lunch,
                self.budget_dinner,
                self.address,
                self.review,
            ],
            self.columns,
        )  # 行を作成
        self.df = self.df.append(se, self.columns)  # データフレームに行を追加
        return


if __name__ == "__main__":
    review = Tabelog(
        base_url="https://tabelog.com/kagawa/rstLst/cake/", test_mode=False
    )
    review.df.to_csv("./review.csv")
