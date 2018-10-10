from ..Module import Module
from ..TagData import TagData


class namestoreExt(Module):
    opmap = {
        'nsExtErrData': 'descend',
    }

### RESPONSE parsing

    def parse_msg(self, response, tag):
        if 'code' in tag.attrib:
            response.set('nsExtErr.code', tag.attrib['code'])
        response.set('nsExtErr.msg', tag.text)

### REQUEST rendering

    def render_default(self, request, data):
        self.render_extension_with_fields(request, 'namestoreExt', [
            TagData('subProduct', data.get('subProduct'))
        ])

