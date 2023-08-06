from sust.api.climate_explorer import clientgen
from sust.api.climate_explorer.clientgen.api import portfolios_api


class Client:
    def __init__(self, api_key, project=None, endpoint=None):
        self._default_req_kwargs = {}
        if project:
            self._default_req_kwargs['project'] = project

        self._openapi_config = clientgen.Configuration(host=endpoint)
        self._openapi_config.api_key['api_key'] = api_key

        openapi_client = clientgen.ApiClient(self._openapi_config)
        self._openapi_instance = portfolios_api.PortfoliosApi(openapi_client)

    def portfolios(self):
        return self._openapi_instance.portfolios_list(**self._default_req_kwargs)

    def assets(self, portfolio_name):
        return PageIterator(self._openapi_instance.portfolios_assets_list, (portfolio_name,), self._default_req_kwargs)

    def physical_risk(self, portfolio_name, scenario=None):
        req_kwargs = self._default_req_kwargs.copy()
        if scenario:
            req_kwargs['scenario'] = scenario

        return PageIterator(self._openapi_instance.portfolios_datasets_physical_items_list, (portfolio_name,), req_kwargs)

    def physical_risk_summary(self, portfolio_name, scenario=None):
        req_kwargs = self._default_req_kwargs.copy()
        if scenario:
            req_kwargs['scenario'] = scenario

        return PageIterator(self._openapi_instance.portfolios_datasets_physical_summary_list, (portfolio_name,), req_kwargs)




class PageIterator:
    def __init__(self, req_func, req_args, req_kwargs):
        self.req_func = req_func
        self.req_args = req_args
        self.req_kwargs = req_kwargs

        self.req_kwargs['page'] = 1
        self.req_kwargs.setdefault('rows', 100)

        self.cache = []
        self.exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.cache) == 0 and not self.exhausted:
            resp = self.req_func(*self.req_args, **self.req_kwargs)
            self.cache = resp

            if len(resp) < self.req_kwargs['rows']:
                self.exhausted = True
            else:
                self.req_kwargs['page'] = self.req_kwargs['page'] + 1

        if len(self.cache) > 0:
            return self.cache.pop(0)

        raise StopIteration
