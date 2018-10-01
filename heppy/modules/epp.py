from ..Module import Module

class epp(Module):
    opmap = {
        'greeting':     'descend',
        'response':     'descend',
        'extension':    'descend',
        'svcMenu':      'descend',
        'svcExtension': 'descend',
        'dcp':          'nothing',
        'svID':         'set',
        'svDate':       'set',
        'lang':         'set',
        'version':      'set',
        'objURI':       'addpair',
        'extURI':       'addpair',
        'value':        'descend',
        'extValue':     'descend',
        'undef':        'nothing',
        'trID':         'descend',
        'clTRID':       'set',
        'svTRID':       'set',
        'resData':      'descend',
    }

### RESPONSE parsing

    def parse_result(self, response, tag):
        response.set('result_code', tag.attrib['code'])
        self.parse_descend(response, tag)

    def parse_msg(self, response, tag):
        if 'lang' in tag.attrib:
            response.set('result_lang', tag.attrib['lang'])
        response.set('result_msg', tag.text)

    def parse_reason(self, response, tag):
        response.set('result_reason', tag.text)

### REQUEST rendering

    def render_login(self, request):
        action = self.render_root_command(request, 'login')

        request.sub(action, 'clID', text=request.get('clID', request.get('login')))
        request.sub(action, 'pw', text=request.get('pw', request.get('password')))
        newPW = request.get('newPW', request.get('newPassword'))
        if newPW is not None:
            request.sub(action, 'newPW', text=newPW)

        options = request.sub(action, 'options')
        request.sub(options, 'version', text=request.get('version', '1.0'))
        request.sub(options, 'lang', text=request.get('lang', 'en'))

        svcs = request.sub(action, 'svcs')
        for svc in request.get('objURIs', [request.nsmap['epp']]):
            request.sub(svcs, 'objURI', text=svc)
        extURIs = request.get('extURIs', [])
        if extURIs:
            exts = request.sub(svcs, 'svcExtension')
            for ext in extURIs:
                request.sub(exts, 'extURI', text=ext)

    def render_logout(self, request):
        self.render_root_command(request, 'logout')

    def render_hello(self, request):
        epp = self.render_epp(request)
        request.sub(epp, 'hello')

    def render_poll(self, request):
        attrs = {'op': request.get('op', 'req')}
        msgID = request.get('msgID')
        if msgID is not None:
            attrs['msgID'] = msgID
        self.render_root_command(request, 'poll', attrs)
