from ..Module import Module
from ..TagData import TagData


class keysys(Module):
    opmap = {
        'resData':      'descend',
        'infData':      'descend',
        'creData':      'descend',
        'renDate':      'set',
        'punDate':      'set',
        'domain-roid':  'set',
        'renewalmode':  'set',
        'transfermode': 'set',
        'transferlock': 'set',
        'contactInfData':'descend',
        'validated':    'set',
        'verification-requested': 'set',
        'verified': 'set',
        'whois-privacy': 'set',
        'es-admin-identificacion': 'set',
        'de-accept-trustee-tac': 'set',
        'es-admin-legalform': 'set',
        'es-admin-tipo-identificacion': 'set',
        'es-billing-identificacion': 'set',
        'es-billing-tipo-identificacion': 'set',
        'es-billing-legalform': 'set',
        'es-tech-identificacion': 'set',
        'es-tech-tipo-identificacion': 'set',
        'es-tech-legalform': 'set',
        'es-owner-identificacion': 'set',
        'es-owner-tipo-identificacion': 'set',
        'es-owner-legalform': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'keysys'

### RESPONSE parsing

    def parse_poll(self, response, tag):
        pass

### REQUEST rendering

    def render_renew(self, request, data):
        ext = self.render_extension(request, 'update')
        domain = request.add_subtag(ext, 'keysys:domain')
        request.add_subtag(domain, 'keysys:renewalmode', {}, data.get('renewalmode'))
        request.add_subtag(domain, 'keysys:transfermode', {}, data.get('transfermode', 'DEFAULT'))

    def render_create(self, request, data):
        pass

    def render_update(self, request, data):
        ext = self.render_extension(request, 'update')
        domain = request.add_subtag(ext, 'keysys:domain')
#        request.add_subtag(domain, 'keysys:accept-trade', {}, '1')

    def render_delete(self, request, data):
        ext = self.render_extension(request, 'delete')
        domain = request.add_subtag(ext, 'keysys:domain')
        request.add_subtag(domain, 'keysys:action', {}, 'push')
        request.add_subtag(domain, 'keysys:target', {}, data.get('target', 'TRANSIT'))

