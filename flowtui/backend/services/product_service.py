from contracts.products import ProductItem

_FAKE_DB = [
    ProductItem(id=1, name="Keyboard", price=99.99),
    ProductItem(id=2, name="Mouse", price=49.99),
    ProductItem(id=3, name="Monitor", price=299.99),
]

class ProductService:
    @staticmethod
    def search(query: str):
        if not query:
            return _FAKE_DB

        q = query.lower()
        return [p for p in _FAKE_DB if q in p.name.lower()]
