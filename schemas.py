from pydantic import BaseModel, Field

class EcommerceItem(BaseModel):
    item_title: str
    item_price: float
    item_extra_info: str

class SchemaNewsWebsites(BaseModel):
    news_headline: str
    news_short_summary: str

class BasicSchema(BaseModel):
    title: str
    content: str