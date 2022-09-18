import json

# Class for HTML Element to scrape
class HtmlElement:
    # Constructor
    def __init__(self,tag:str,attr:str,val:str,extra_elem:str=None) -> object:
        self.tag=tag
        self.attr=attr
        self.val=val
        self.extra_elem=extra_elem

# Class for Raspberry Pi
class RaspPi:
    # Constructor
    def __init__(self,model:str,price:float,available:str,url_ref:int) -> object:
        self.model=model
        self.price=price
        self.available=available
        self.url_ref=url_ref
    
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