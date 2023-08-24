import logging
import os
import re
import subprocess
import uuid
from copy import deepcopy
from functools import singledispatchmethod
from pathlib import Path
from typing import Iterable, Mapping, Union

from cloudmesh.common import FlatDict

from .utils import get_fragment_cache_path, get_model_repo_cache_path


def _get_fragment_path(fragment: Mapping):
    cchpth, fname = get_fragment_cache_path(fragment, create=False)
    # The tar files will be unpacked already
    if os.path.splitext(fname)[-1] == ".tar":
        fname = fname[:-4]
    lfname = os.path.join(cchpth, fname)
    return lfname

def _get_repo_path(model: Mapping):
    cchpth, repo = get_model_repo_cache_path(model, create=False)
    repopath = os.path.join(cchpth, repo)
    return repopath

def _compile_dataset_fragments(dataset : Mapping):
    """Creates a dictionary to access dataset fragments by ID"""
    dataset_context = {}
    if 'fragments' in dataset:
        for fragment in dataset['fragments']:
            fragment_id = fragment['id']
            if fragment_id in dataset_context:
                logging.warning("In dataset %s there are multiple fragments with id: %s", dataset['name'], fragment_id)
            dataset_context[fragment['id']] = _get_fragment_path(fragment)
    else:
        dataset_context['main'] = _get_fragment_path()
    return dataset_context 

class ContextExecutor:
    """
    Executes command templates substituting {} parameters using provided 
    context. Default context is created from config and dataset 
    """
    def __init__(self, config, model, dataset):
        self.context = {}
        self.config = config
        # TODO: add check for required keys model_name, dataset_name
        self.context['config'] = config
        self.context['source'] = _get_repo_path(model) 
        self.context['dataset'] = _compile_dataset_fragments(dataset)

    def prepare_workdir(self, workdir=None):
        """Creates a new unique working directory or ensures that the provided one exists"""
        if workdir is None:
            workdir = '_'.join(['run', self.config['model_name'], self.config['dataset_name'], uuid.uuid4().hex])
        os.makedirs(workdir, exist_ok=True)
        return workdir
    
    @singledispatchmethod
    def execute(self, commands : Iterable[str], context : Mapping, dryrun=False):
        context = deepcopy(self.context)
        context.update(context)
        context = FlatDict(context, sep='.')
        # TODO: if we have different command sets, ensure workdir is unique
        workdir = self.prepare_workdir(self.config.get('workdir'))
        for command in commands:
            command = context.apply(command)
            if re.match("\{[^ ]\}", command):
                logging.waning("Failed to substitute all template parameters: '%s'", command)
            
            if dryrun:
                logging.info("Executing [dry run]: '%s'", command)
            else:
                logging.info("Executing: '%s'", command)
                subprocess.run(command, shell=True, check=True, cwd=workdir) # Will raise exception if command failed 
        
    @execute.register
    def execute_str(self, commands : str, context : Mapping, dryrun=False):
        return self.execute([commands], context, dryrun=False)