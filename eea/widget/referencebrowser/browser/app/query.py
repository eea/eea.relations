from eea.facetednavigation.browser.app.query import FacetedQueryHandler

class FacetedQuery(FacetedQueryHandler):
    """ Faceted Query
    """
    def criteria(self, sort=True, **kwargs):
        """ Process catalog query
        """
        query = {}

        # Portal type
        field = self.context.getField('ct_type')
        value = field.getAccessor(self.context)()
        if value:
            query['portal_type'] = value

        # Object provides
        field = self.context.getField('ct_interface')
        value = field.getAccessor(self.context)()
        if value:
            query['object_provides'] = value

        # Update query from faceted navigation configuration
        query.update(
            super(FacetedQuery, self).criteria(sort, **kwargs)
        )
        return query
