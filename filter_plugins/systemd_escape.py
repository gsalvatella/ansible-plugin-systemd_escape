from ansible.errors import AnsibleFilterError
import subprocess

SYSTEMD_ESCAPE = 'systemd-escape'


def do_escape(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        raise AnsibleFilterError(
            'Error in subprocess.run in systemd_escape filter plugin:\n%s' % e)

    return res.stdout.rstrip('\n')


def systemd_escape(s, suffix=None, template=None, path=False, mangle=False):

    cmd = [SYSTEMD_ESCAPE]

    if suffix and (template or mangle) or (template and mangle):
        raise AnsibleFilterError(
            "Options suffix, template, and mangle are mutually exclusive.")

    if suffix:
        cmd.append(f'--suffix={suffix}')
    elif template:
        cmd.append(f'--template={template}')
    elif mangle:
        cmd.append('--mangle')

    if path:
        cmd.append('--path')

    cmd.append(s)

    return do_escape(cmd)


def systemd_unescape(s, path=False):

    cmd = [SYSTEMD_ESCAPE]

    if path:
        cmd.append(' --path')

    cmd.append(s)

    return do_escape(cmd)


class FilterModule(object):
    def filters(self):
        return {
            'systemd_escape': systemd_escape,
            'systemd_unescape': systemd_unescape
        }
