import os
import subprocess
import csv
import pathlib
import urllib
import argparse


def run_list(dataType='on_resonance'):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'data/{dataType}.dat')) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield urllib.parse.urlencode(row)


def url_list(
        dataType='on_resonance',
        eventTypes=['evtgen-uds', 'evtgen-charm', 'evtgen-charged', 'evtgen-mixed'],
        stream_cardinal=0,
        exs=None,
        data=False,
    ):
    for runs in run_list():
        ex = int(urllib.parse.parse_qs(runs)['ex'][0])
        if exs and ex not in exs: continue
        if data:
            skim = 'HadronB'  if ex < 20 else 'HadronBJ'
            yield f'http://bweb3/mdst.php?{runs}&skm={skim}&dt={dataType}&bl=caseB'
        else:
            stream_base = 10 if ex < 30 else 0
            stream = stream_base + stream_cardinal
            for eventType in eventTypes:
                yield f'http://bweb3/montecarlo.php?{runs}&ty={eventType}&dt={dataType}&bl=caseB&st={stream}'


class SubmitInfo:

    def __init__(self, args=None):
        self.parser = _build_parser()
        self.args = self.parser.parse_args() if args is None else self.parser.parse_args(args.split())

        self.output_directory_path = pathlib.Path(self.args.outputDir)
        self.output_directory_path.mkdir(parents=True, exist_ok=True)

        self._startsWithHttp = len(self.args.path) == 1 and self.args.path[0].startswith('http://')
        self._parse_result = urllib.parse.urlparse(self.url) if self._startsWithHttp else None

    @property
    def isCustomFile(self):
        return not self._startsWithHttp

    @property
    def url(self):
        return self.args.path if self.isCustomFile else self.args.path[0]

    @property
    def isMC(self):
        return self.isCustomFile or self._parse_result.path == '/montecarlo.php'

    @property
    def outputname(self):
        directory = self.output_directory_path.absolute().as_posix()
        labels = (self.args.path[0].strip('.mdst').split('/')[:-1] if self.isCustomFile
                else [value[0] for value in urllib.parse.parse_qs(self._parse_result.query).values()])
        if self.args.suffix: labels.extend([self.args.suffix])
        basename = '_'.join(labels)
        return f'{directory}/{basename}.root'


def _build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
        default=['http://bweb3/montecarlo.php?ex=55&rs=990&re=1093&ty=evtgen-uds&dt=on_resonance&bl=caseB&st=0'],
        nargs='+')
    parser.add_argument('--suffix', default='')
    parser.add_argument('--outputDir', default='.')
    return parser


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('steering')
    parser.add_argument('--outputDir', default='.')
    parser.add_argument('--queue', default='s')
    parser.add_argument('--data', action='store_true', default=False)
    parser.add_argument('--eventTypes', nargs='+', default=['evtgen-uds', 'evtgen-charm', 'evtgen-charged', 'evtgen-mixed'])
    parser.add_argument('--exs', nargs='+', default=None, type=int)
    parser.add_argument('--dry-run', dest='out', action='store_const', const=print, default=subprocess.run)
    args = parser.parse_args()

    for url in url_list(data=args.data, eventTypes=args.eventTypes, exs=args.exs):
        args.out(f'bsub -q {args.queue} {args.steering} -- --path {url} --outputDir {args.outputDir}'.split())

