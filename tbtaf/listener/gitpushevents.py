import requests
import json

from argparse import Namespace

class GitPushEvents(object):
    def get_latest(token, base_url, user, repo, latest_id):
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'token {token}',
        }

        response = requests.get(
            f'{base_url}/{user}/{repo}/events?type=PushEvents', headers=headers)
        events = json.loads(
            response.content, object_hook=lambda d: Namespace(**d))
        events.sort(key=id, reverse=True)

        final_events = list(filter(lambda ev: int(ev.id) > latest_id, events))
        if len(final_events) > 0:
            print(final_events[0])
            return final_events[0]
        else:
            return None
