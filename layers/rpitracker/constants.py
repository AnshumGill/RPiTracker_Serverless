from models import *

# User Agent used for making requests
headers={
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

# Defining vendor objects
vendors=[
    Vendor(
        "SilverLine",
        ["https://www.silverlineelectronics.in/collections/raspberry-pi-4/products/raspberry-pi-4-model-b-4gb-silverline-india",
        "https://www.silverlineelectronics.in/collections/the-raspberry-pi/products/raspberry-pi-4-model-b-2gb",
        "https://www.silverlineelectronics.in/collections/raspberry-pi-4/products/raspberry-pi-4-model-b-8gb-silverline-india"],
         False,
         HtmlElement("h1","itemprop","name"), # Model Element
         HtmlElement("span","itemprop","price"), # Price Element 
         HtmlElement("p","class","product-inventory","span") # Stock availablity Element
    ),
    Vendor(
        "FactoryForward",
        ["https://www.factoryforward.com/product/raspberry-pi-4-model-b-4gb/",
        "https://www.factoryforward.com/product/raspberry-pi-4-model-b-2gb/",
        "https://www.factoryforward.com/product/raspberry-pi-4-model-b-8gb/"],
         True,
         HtmlElement("h2","class","product_title"), # Model Element
         HtmlElement("span","class","woocommerce-Price-amount amount"), # Price Element 
         HtmlElement("span","class","stock") # Stock availablity Element
    ),
    Vendor(
        "Robu",
        ["https://robu.in/product/raspberry-pi-4-model-b-with-4-gb-ram",
        "https://robu.in/product/raspberry-pi-4-model-b-with-2-gb-ram",
        "https://robu.in/product/raspberry-pi-4-model-b-with-8-gb-ram"],
         True,
         HtmlElement("h1","class","product_title"), # Model Element
         HtmlElement("span","class","electro-price"), # Price Element 
         HtmlElement("p","class","stock") # Stock availablity Element
    ),
    Vendor(
        "Robocraze",
        ["https://robocraze.com/products/raspberry-pi-4-model-b-4gb-ram",
        "https://robocraze.com/products/raspberry-pi-4-model-b-2gb-ram",
        "https://robocraze.com/products/raspberry-pi-4-model-b-8-gb-ram"],
         True,
         HtmlElement("h1","class","product-single__title"), # Model Element
         HtmlElement("span","class","price-item price-item--sale"), # Price Element 
         HtmlElement("button","class","product-form__cart-submit") # Stock availablity Element
    )
]

# Table name for dynamodb
dynamodb_table="tf_rpiTracker"