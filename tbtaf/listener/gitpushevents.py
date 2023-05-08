import requests
import json

from argparse import Namespace

'''
Class for communicate with Git Events API and query for Push events
'''
class GitPushEvents(object):
    FIRST_EVENT = 0
    
    '''
    Gets the latest push event of a given repository, if find someone new, returns the event payload
    '''
    def get_latest(token, base_url, user, repo, latest_id):
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'token {token}',
        }

        response = requests.get(
            f'{base_url}/{user}/{repo}/events?type=PushEvents', headers=headers)
        events = json.loads(
            response.content, object_hook=lambda d: Namespace(**d))
        print(str(events))
        events.sort(key=id, reverse=True)

        final_events = list(filter(lambda ev: int(ev.id) > latest_id, events))
        if len(final_events) > 0:
            print(final_events[GitPushEvents.FIRST_EVENT])
            return final_events[GitPushEvents.FIRST_EVENT]
        else:
            return None
