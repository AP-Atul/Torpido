import json
import subprocess
import os

from ._exceptions import ProbeException

__all__ = ['probe']


def probe(filename, cmd='ffprobe', timeout=None):
    """Runs the ffprobe on the given file and outputs in json format """

    # check if file exists
    if not os.path.isfile(filename):
        raise FileExistsError(f"Input file: {filename} does not exits.")

    args = [cmd, '-show_format', '-show_streams', '-of', 'json']
    args += [filename]

    p = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

    communicate_kwargs = {}
    if timeout is not None:
        communicate_kwargs['timeout'] = timeout

    out, err = p.communicate(**communicate_kwargs)

    if p.returncode != 0:
        raise ProbeException('ffprobe', out, err)

    return json.loads(out.decode('utf-8'))


