import random
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import List, Optional, Tuple


Product = Tuple[int, str, int]


class ProductList:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = Path(db_path) if db_path else Path(__file__).with_name("MyProduct.db")
        self.create_table()

    def create_table(self) -> None:
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Products (
                        productID INTEGER PRIMARY KEY,
                        productName TEXT NOT NULL,
                        productPrice INTEGER NOT NULL
                    )
                    """
                )

    def insert_product(self, product_id: int, product_name: str, product_price: int) -> None:
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                connection.execute(
                    """
                    INSERT INTO Products (productID, productName, productPrice)
                    VALUES (?, ?, ?)
                    """,
                    (product_id, product_name, product_price),
                )

    def update_product(self, product_id: int, product_name: str, product_price: int) -> int:
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    UPDATE Products
                    SET productName = ?, productPrice = ?
                    WHERE productID = ?
                    """,
                    (product_name, product_price, product_id),
                )
                return cursor.rowcount

    def delete_product(self, product_id: int) -> int:
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                cursor = connection.execute(
                    "DELETE FROM Products WHERE productID = ?",
                    (product_id,),
                )
                return cursor.rowcount

    def select_products(self, product_id: Optional[int] = None) -> List[Product]:
        with closing(sqlite3.connect(self.db_path)) as connection:
            if product_id is None:
                cursor = connection.execute(
                    """
                    SELECT productID, productName, productPrice
                    FROM Products
                    ORDER BY productID
                    """
                )
            else:
                cursor = connection.execute(
                    """
                    SELECT productID, productName, productPrice
                    FROM Products
                    WHERE productID = ?
                    """,
                    (product_id,),
                )
            return cursor.fetchall()

    def insert_sample_data(self) -> int:
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                existing_products = connection.execute(
                    """
                    SELECT productID, productName, productPrice
                    FROM Products
                    ORDER BY productID
                    """
                ).fetchall()
                old_sample = len(existing_products) == 1000 and all(
                    product == (
                        product_id,
                        "전자제품 {:04d}".format(product_id),
                        10000 + product_id * 100,
                    )
                    for product_id, product in enumerate(existing_products, start=1)
                )
                if existing_products and not old_sample:
                    return 0
                if old_sample:
                    connection.execute("DELETE FROM Products")

                catalog = [
                    ("스마트폰", [
                        "Apple iPhone 16 128GB", "Apple iPhone 16 Pro 256GB",
                        "Apple iPhone 16 Pro Max 256GB", "삼성전자 갤럭시 S24 256GB",
                        "삼성전자 갤럭시 S24 Ultra 256GB", "삼성전자 갤럭시 Z Flip6 256GB",
                        "삼성전자 갤럭시 Z Fold6 512GB", "삼성전자 갤럭시 A55 128GB",
                        "Google Pixel 9 128GB", "Xiaomi 14T 256GB",
                    ], 450_000, 2_400_000),
                    ("노트북", [
                        "삼성전자 갤럭시북4 Pro 16형", "삼성전자 갤럭시북4 15형",
                        "LG gram Pro 16 2024", "LG gram 15 2024",
                        "Apple MacBook Air 13 M3 16GB 512GB",
                        "Apple MacBook Pro 14 M3 Pro", "Lenovo ThinkPad E14 Gen 6",
                        "Lenovo IdeaPad Slim 5 16", "ASUS Zenbook 14 OLED",
                        "ASUS Vivobook 16",
                    ], 750_000, 4_500_000),
                    ("태블릿", [
                        "Apple iPad Air 11형 M2", "Apple iPad Pro 11형 M4",
                        "Apple iPad 10세대 64GB", "삼성전자 갤럭시 탭 S9 FE",
                        "삼성전자 갤럭시 탭 S9 256GB", "삼성전자 갤럭시 탭 S9 Ultra",
                        "Lenovo Tab P12", "Lenovo Legion Tab", "Xiaomi Pad 6",
                        "Microsoft Surface Go 4",
                    ], 300_000, 2_200_000),
                    ("TV", [
                        "삼성전자 Crystal UHD 55형", "삼성전자 QLED 65형",
                        "삼성전자 Neo QLED 65형", "삼성전자 OLED 77형",
                        "LG전자 울트라HD 55형", "LG전자 QNED 65형",
                        "LG전자 OLED evo 65형", "LG전자 OLED evo 77형",
                        "TCL QLED 65형", "Sony BRAVIA XR 65형",
                    ], 500_000, 8_500_000),
                    ("모니터", [
                        "삼성전자 Smart Monitor M7 32형", "삼성전자 Odyssey G5 27형",
                        "삼성전자 Odyssey OLED G8 34형", "LG전자 울트라기어 27GP850",
                        "LG전자 울트라와이드 34WP65C", "Dell UltraSharp U2723QE",
                        "Dell Alienware AW3423DWF", "BenQ PD2705U",
                        "ASUS ROG Swift PG27AQDM", "알파스캔 AOC Q27G2S",
                    ], 180_000, 2_000_000),
                    ("이어폰·헤드폰", [
                        "Apple AirPods 4", "Apple AirPods Pro 2세대",
                        "삼성전자 갤럭시 버즈 FE", "삼성전자 갤럭시 버즈3 Pro",
                        "Sony WF-1000XM5", "Sony WH-1000XM5",
                        "Bose QuietComfort Ultra Headphones",
                        "JBL Tune 770NC", "Sennheiser Momentum 4 Wireless",
                        "Audio-Technica ATH-M50x",
                    ], 50_000, 750_000),
                    ("스마트워치", [
                        "Apple Watch SE 2세대 40mm", "Apple Watch Series 9 45mm",
                        "Apple Watch Ultra 2", "삼성전자 갤럭시 워치6 40mm",
                        "삼성전자 갤럭시 워치6 Classic 47mm",
                        "삼성전자 갤럭시 워치 FE", "Garmin Forerunner 265",
                        "Garmin Venu 3", "Fitbit Charge 6", "Google Pixel Watch 2",
                    ], 100_000, 1_300_000),
                    ("카메라", [
                        "Canon EOS R50 RF-S18-45mm", "Canon EOS R8 Body",
                        "Canon EOS R6 Mark II Body", "Nikon Z fc 16-50mm",
                        "Nikon Z6 III Body", "Sony Alpha 6400 16-50mm",
                        "Sony Alpha 7 IV Body", "Sony ZV-E10 II 16-50mm",
                        "Fujifilm X-S20 Body", "Fujifilm X100VI",
                    ], 650_000, 5_500_000),
                    ("생활가전", [
                        "삼성전자 비스포크 냉장고 4도어 875L",
                        "LG전자 디오스 오브제컬렉션 냉장고 870L",
                        "삼성전자 비스포크 그랑데 세탁기 24kg",
                        "LG전자 트롬 오브제컬렉션 세탁기 25kg",
                        "삼성전자 비스포크 건조기 20kg",
                        "LG전자 퓨리케어 공기청정기 360도",
                        "삼성전자 무풍에어컨 스탠드형",
                        "LG전자 휘센 오브제컬렉션 에어컨",
                        "삼성전자 비스포크 식기세척기 14인용",
                        "LG전자 디오스 광파오븐",
                    ], 350_000, 5_500_000),
                    ("주방·청소가전", [
                        "다이슨 V12 Detect Slim", "다이슨 Gen5 디텍트",
                        "삼성전자 비스포크 제트 AI", "LG전자 코드제로 오브제컬렉션 A9",
                        "로보락 S8 MaxV Ultra", "에코백스 디봇 T30 Pro Omni",
                        "쿠쿠 트윈프레셔 밥솥 10인용", "쿠첸 브레인 밥솥 6인용",
                        "발뮤다 더 토스터", "필립스 에어프라이어 XXL",
                    ], 120_000, 2_500_000),
                ]
                sellers = [
                    "공식 온라인몰", "쿠팡", "네이버쇼핑", "11번가", "G마켓",
                    "SSG닷컴", "롯데ON", "전자랜드", "하이마트", "오늘의집",
                ]
                rng = random.Random(20261028)
                offers = []
                for _, names, minimum_price, maximum_price in catalog:
                    for name in names:
                        base_price = rng.randrange(
                            minimum_price // 1000,
                            maximum_price // 1000 + 1,
                        ) * 1000
                        for seller in sellers:
                            price_rate = rng.uniform(0.90, 1.08)
                            price = round(base_price * price_rate / 1000) * 1000
                            offers.append(("{} - {}".format(name, seller), price))
                rng.shuffle(offers)
                products = [
                    (product_id, name, price)
                    for product_id, (name, price) in enumerate(offers, start=1)
                ]
                connection.executemany(
                    """
                    INSERT INTO Products (productID, productName, productPrice)
                    VALUES (?, ?, ?)
                    """,
                    products,
                )
                return len(products)


if __name__ == "__main__":
    products = ProductList()
    inserted_count = products.insert_sample_data()
    print("샘플 데이터 {}건을 추가했습니다.".format(inserted_count))
    print("현재 등록된 제품 수:", len(products.select_products()))
    print("첫 번째 제품:", products.select_products(1)[0])
