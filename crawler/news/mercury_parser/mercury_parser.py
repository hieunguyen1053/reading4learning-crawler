import json
import os
import subprocess
import tempfile
from typing import Union

DIR = os.path.dirname(os.path.realpath(__file__))


class MercuryParser:
    def parse(self, url: str, options: Union[str, dict] = {}):
        if isinstance(options, dict):
            options = json.dumps(options)

        option_tmp = tempfile.NamedTemporaryFile(suffix='.json')

        option_tmp.write(options.encode('utf-8'))
        option_tmp.flush()

        cmd = [
            'node',
            'mercury-parser.js',
            url,
            option_tmp.name,
        ]
        process = subprocess.Popen(cmd, cwd=DIR, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        output = output.decode('utf-8')
        output = json.loads(output)
        return output


if __name__ == '__main__':
    parser = MercuryParser()
    print(parser.parse('https://www.cnbc.com/2022/01/11/powell-says-rate-hikes-tighter-policy-will-be-needed-to-control-inflation.html', {}))
