from ..Module import Module
from ..TagData import TagData


class host(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'roid':         'set',
        'name':         'set',
        'clID':         'set',
        'crID':         'set',
        'upID':         'set',
        'crDate':       'set',
        'upDate':       'set',
        'exDate':       'set',
        'trDate':       'set',
    }

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

    def parse_addr(self, response, tag):
        response.add_list('ips', tag.text)

### REQUEST rendering

    def render_check(self, request, data):
        self.render_check_command(request, data, 'name')

    def render_info(self, request, data):
        self.render_command_with_fields(request, 'info', [
            TagData('name', data.get('name'))
        ])

    def render_create(self, request, data):
        command = self.render_command_with_fields(request, 'create', [
            TagData('name', data.get('name'))
        ])
        self.render_ips(request, data.get('ips', []), command)

    def render_delete(self, request, data):
        self.render_command_with_fields(request, 'delete', [
            TagData('name', data.get('name'))
        ])

    def render_update(self, request, data):
        command = self.render_command_with_fields(request, 'update', [
            TagData('name', data.get('name'))
        ])

        if 'add' in data:
            self.render_update_section(request, data.get('add'), command, 'add')
        if 'rem' in data:
            self.render_update_section(request, data.get('rem'), command, 'rem')
        if 'chg' in data:
            self.render_update_section(request, data.get('chg'), command, 'chg')

    def render_update_section(self, request, data, command, operation):
        element = request.add_subtag(command, 'host:' + operation)
        if operation == 'chg':
            request.add_subtag(element, 'host:name', text=data.get('name'))
        else:
            self.render_ips(request, data.get('ips', []), element)
            self.render_statuses(request, element, data.get('statuses', {}))

    def render_ips(self, request, ips, parent):
        for ip in ips:
            request.add_subtag(parent, 'host:addr', {'ip': 'v6' if ':' in ip else 'v4'}, ip)
