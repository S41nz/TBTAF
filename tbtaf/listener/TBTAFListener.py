import logging
import shutil
import os

import configparser
from git import Repo

from listener.gitpushevents import GitPushEvents
from orchestrator.TBTAFOrchestrator import TBTAFOrchestrator


class Listener(object):
      
    def check_push_events(self):
        logging.info("Getting configuration...")
        
        config = configparser.ConfigParser()
        config.read('listener/listener.properties')

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
        
        orchestrator = TBTAFOrchestrator()
        
        testScript = "./test/test05.tbtaf"
        
        print("Welcome to TBTAF Test bed")
        
        print("Executing the following test script: " + testScript)
        
        parseResult = orchestrator.parseScript(testScript)

        print("Parse Status: "+parseResult.status)

        print("Parse Message"+parseResult.message)


        if event != None:
            logging.info(f'New event Found! ID: {event.id}')
            if os.path.exists(f'{path_to_clone}{event.id}'):
                logging.info('Old local version of the same event, removing it...')
                shutil.rmtree(f'{path_to_clone}{event.id}')
            
            logging.info(f'Cloning {event.repo.url.replace("api.", "").replace("repos/", "")}.git ...')
            repo = Repo.clone_from(
                f'{event.repo.url.replace("api.", "").replace("repos/", "")}.git',
                f'{path_to_clone}{event.id}/',
                branch=f'{event.payload.ref.split("/")[2]}'
            )
            logging.info(f'Cloned {event.repo.url.replace("api.", "").replace("repos/", "")}.git')
            
            testScript = "./test/test05.tbtaf"
            print("Welcome to TBTAF Test bed")
            
            myTBTAF = TBTAFOrchestrator()
            
            print("Executing the following test script: " + testScript)
            
            parseResult = myTBTAF.parseScript(testScript)

            print("Parse Status: "+parseResult.status)

            print("Parse Message"+parseResult.message)
            
            logging.info('Persisting ID..')
            config.set('IDs', 'latest_id', str(event.id))
            with open('listener.properties', 'w') as configfile:
                config.write(configfile)
            logging.info('ID Persisted')
            return True
        else:
            logging.info('No new events detected')
            return False
    
    
    if __name__ == '__main__':
        logging.basicConfig(filename='listener.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
        
        check_push_events()
