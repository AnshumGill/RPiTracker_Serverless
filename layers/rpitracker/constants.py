from models import *

headers={
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

vendors=[
    Vendor(
        "SilverLine",
        ["https://www.silverlineelectronics.in/collections/raspberry-pi-4/products/raspberry-pi-4-model-b-4gb-silverline-india"],
         False,
         HtmlElement("h1","itemprop","name"),
         HtmlElement("span","itemprop","price"),
         HtmlElement("p","class","product-inventory","span")
    ),
    Vendor(
        "FactoryForward",
        ["https://www.factoryforward.com/product/raspberry-pi-4-model-b-4gb/"],
         True,
         HtmlElement("h2","class","product_title"),
         HtmlElement("span","class","woocommerce-Price-amount amount"),
         HtmlElement("span","class","stock")
    ),
    Vendor(
        "Robu",
        ["https://robu.in/product/raspberry-pi-4-model-b-with-4-gb-ram"],
         True,
         HtmlElement("h1","class","product_title"),
         HtmlElement("span","class","electro-price"),
         HtmlElement("p","class","stock")
    ),
    Vendor(
        "Robocraze",
        ["https://robocraze.com/products/raspberry-pi-4-model-b-4gb-ram"],
         True,
         HtmlElement("h1","class","product-single__title"),
         HtmlElement("span","class","price-item price-item--sale"),
         HtmlElement("button","class","product-form__cart-submit")
    )
]

oos_strings=["out of stock","sold out"]