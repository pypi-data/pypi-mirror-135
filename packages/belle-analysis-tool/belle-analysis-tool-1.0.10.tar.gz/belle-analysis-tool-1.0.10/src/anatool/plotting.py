from contextlib import contextmanager
import subprocess
import os
import ROOT as R


@contextmanager
def canvas_upload(name='c', title='', w=1600, h=900, ncols=1, nrows=1, local_path=None, remote_path='.', keep_local_file=False):
    c = R.TCanvas(name, title, w, h)
    c.Divide(ncols, nrows)
    yield c
    fname = local_path if local_path else name + '.pdf'
    c.SaveAs(fname)
    R.gDirectory.Delete(name)
    subprocess.run(f'{os.path.expanduser("~/dropbox_uploader.sh")} upload {fname} {remote_path}'.split())
    if not keep_local_file:
        os.remove(fname)


def pretty_draw(frame):
    frame.GetXaxis().CenterTitle()
    frame.GetYaxis().CenterTitle()
    frame.GetYaxis().SetMaxDigits(3)
    frame.Draw()


import os
import abc
import sys
import configparser

import ROOT
import matplotlib as mpl
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.config/anatool.cfg'))


class IUploader(abc.ABC):

    @abc.abstractmethod
    def upload(self, local_path, remote_path):
        pass


class DropboxUploader(IUploader):

    def __init__(self):
        self._dbx = dropbox.Dropbox(config['OAUTH_ACCESS_TOKEN']['DROPBOX'])
        try:
            self._dbx.users_get_current_account()
        except AuthError:
            sys.exit('ERROR: Invalid access token; try re-generating an access'
                     'token from the app console on the web.')
            
    def upload(self, local_path, remote_path=None):
        if remote_path is None:
            remote_path = '/' + os.path.basename(local_path)
        with open(local_path, 'rb') as f:
            try:
                self._dbx.files_upload(f.read(), remote_path, mode=WriteMode('overwrite'))
            except ApiError as err:
                print(err)
                sys.exit()


class CanvasAdapter:

    def __init__(self, canvas):
        self._canvas = canvas

    def save(self):
        if isinstance(self._canvas, ROOT.TCanvas):
            fname = self._canvas.GetName() + '.pdf'
            self._canvas.SaveAs(fname)
            return fname
        elif isinstance(self._canvas, mpl.figure.Figure):
            fname = self._canvas.get_label() + '.pdf'
            self._canvas.savefig(fname)
            return fname


class Uploader:

    def __init__(self, uploader: IUploader = DropboxUploader()):
        self._canvases = []
        self._uploader = uploader

    def register(self, canvas):
        self._canvases.append(CanvasAdapter(canvas))

    def upload(self):
        for canvas in self._canvases:
            fname = canvas.save()
            self._uploader.upload(fname)

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        self.upload()


