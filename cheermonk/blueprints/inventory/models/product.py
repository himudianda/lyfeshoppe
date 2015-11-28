from cheermonk.lib.util_sqlalchemy import ResourceMixin
from cheermonk.extensions import db


class Product(ResourceMixin, db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)

    # Relationships.
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id',
                                                      onupdate='CASCADE',
                                                      ondelete='CASCADE'),
                            index=True, nullable=False)

    # Product Details.
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    price = db.Column(db.Integer())

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (cls.title.ilike(search_query))

        return search_chain

    @classmethod
    def create(cls, params):
        """
        Return whether or not the product was created successfully.

        :return: bool
        """

        product = Product(**params)
        db.session.add(product)
        db.session.commit()

        return True
