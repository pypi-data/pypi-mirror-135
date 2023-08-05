import os
import mxdevtool as mx
from mxdevtool.data.repositories.repo import Repository, DefaultRepository


def init():
    global repo_list
    global default_repo
    repo_list = []
    default_repo = DefaultRepository.instance()


def get_repo() -> Repository:
    try:
        return repo_list[0]
    except:
        return DefaultRepository.instance()


def set_repo(repo):
    init()
    repo_list.clear()
    repo_list.append(repo)

    # calendar setting
    repo.load_configuration_calendar()
