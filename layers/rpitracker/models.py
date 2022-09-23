import json
from re import sub
# Class for HTML Element to scrape
class HtmlElement:
    # Constructor
    def __init__(self,tag:str,attr:str,val:str,extra_elem:str=None) -> object:
        self.tag=tag
        self.attr=attr
        self.val=val
        self.extra_elem=extra_elem
        self.content=None

    # Method to scrape content for HTML Element
    def scrape_content(self,soup):
        self.content=soup.find(self.tag,{self.attr:self.val})
        if(self.content is not None):
            if(self.extra_elem!=None):
                self.content=self.content.find(self.extra_elem)
            self.content=self.content.text.strip()

# Class for Raspberry Pi
class RaspPi:
    # Constructor
    def __init__(self,model:HtmlElement,price:HtmlElement,available:HtmlElement,url_ref:int,gst_inc=None,notified:bool=False) -> object:
        self.model=model.content
        self.price=price.content
        self.available=available.content
        self.url_ref=url_ref
        self.gst_inc=gst_inc
        self.notified=notified
        self.update_avail(["out of stock","sold out"])
        self.update_price()

    # Method to update availablity to Boolean type
    def update_avail(self,oos_strings):
        if('-' in self.available):
            self.available=self.available.split('-')[0].strip()
        self.available=not(self.available.lower() in oos_strings)

    # Method to update price to appropriate format
    def update_price(self):
        self.price=sub("[^0-9.]","",self.price) # Removing all values except numbers and period
        self.price=float(self.price[1:] if self.price[0]=="." else self.price) # Removing trailing period if exists
        self.price=self.price if self.gst_inc else self.price*1.18 # Including GST%

    # Notified or not
    def mark_notified(self,val):
        self.notified=val
    
    # Method to determine equality
    def __eq__(self,other):
        return self.model == other

# Class for website. Many to one relation with RasPi
class Vendor:
    # Constructor
    def __init__(self,name:str,urls:list,gst_inc:bool,model_elem:HtmlElement,price_elem:HtmlElement,stock_elem:HtmlElement) -> object:
        self.name=name
        self.urls=urls
        self.gst_inc=gst_inc
        self.model_elem=model_elem
        self.price_elem=price_elem
        self.stock_elem=stock_elem
        self.raspi=[]

    # Linking Raspberry Pi to Vendor
    def add_raspi(self,raspi: RaspPi):
        if(raspi not in self.raspi):
            self.raspi.append(raspi)
    
    # Serializing Object
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o:o.__dict__,
            sort_keys=True
        )