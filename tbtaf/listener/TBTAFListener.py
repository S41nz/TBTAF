import logging
import shutil
import os

import configparser
from git import Repo

from listener.gitpushevents import GitPushEvents
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator


class TBTAFListener(object):
    BRANCH_POSITION = 2
    
    '''
    Constructor
    '''
    def __init__(self):
        logging.basicConfig(filename='listener.log', level=logging.DEBUG,
                            format='%(asctime)s [%(levelname)s] %(message)s')
    '''
    Check the push events through the Github Api access manager class
    if some event is found, the affected repository and branch are cloned
    and the test script is executed
    '''
    def check_push_events(self, testScript, propertiesFilePath='listener/listener.properties'):
        logging.info("Getting configuration...")

        config = configparser.ConfigParser()
        config.read(propertiesFilePath)
        
        if not os.path.exists(propertiesFilePath):
            logging.error(f'File {propertiesFilePath} not located')
            return

        token = config.get('RepositoryToListen', 'token')
        base_url = config.get('RepositoryToListen', 'base_url')
        user = config.get('RepositoryToListen', 'user')
        repo = config.get('RepositoryToListen', 'repo')
        path_to_clone = config.get('RepositoryCloning', 'local_path')
        logging.info('Configuration loaded')

        logging.info('Getting last listened push event ID...')
        latest_id = int(config.get('IDs', 'latest_id'))
        logging.info(f'Last listened push event ID: <<{latest_id}>>')

        logging.info('Checking if there are new event wit Github API')
        event = GitPushEvents.get_latest(
            token=token, base_url=base_url, user=user, repo=repo, latest_id=latest_id)
        logging.info(f'Checked in {base_url}/{user}/{repo}')
        if event != None:
            logging.info(f'New event Found! ID: {event.id}')
            if os.path.exists(f'{path_to_clone}{event.id}'):
                logging.info('Old local version of the same event, removing it...')
                shutil.rmtree(f'{path_to_clone}{event.id}')
            logging.info(f'Cloning {event.repo.url.replace("api.", "").replace("repos/", "")}.git ...')
            repo = Repo.clone_from(
                f'{event.repo.url.replace("api.", "").replace("repos/", "")}.git',
                f'{os.path.expanduser("~")}/{path_to_clone}{event.id}/',
                branch=f'{event.payload.ref.split("/")[TBTAFListener.BRANCH_POSITION]}'
            )
            logging.info(f'Cloned {event.repo.url.replace("api.", "").replace("repos/", "")}.git')
            if os.path.exists(testScript):
                self.run_test(testScript)
            else:
                logging.error(f'File {testScript} not located')
            logging.info('Persisting ID..')
            config.set('IDs', 'latest_id', str(event.id))
            with open('listener.properties', 'w') as configfile:
                config.write(configfile)
            logging.info('ID Persisted')
            return True
        else:
            logging.info('No new events detected')
            return False
    
    '''
    Run the test script if some event is found
    '''
    def run_test(self, testScript):
        print("Welcome to TBTAF Test bed")
        myTBTAF = TBTAFOrchestrator()
        print(f"Executing the following test script: {testScript}")
        parseResult = myTBTAF.parseScript(testScript)
        print(f"Parse Status: {parseResult.status}")
        print(f"Parse Message: {parseResult.message}")
