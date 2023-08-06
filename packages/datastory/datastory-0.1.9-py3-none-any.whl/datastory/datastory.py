import json
import os
import requests
import plotly
import webbrowser

from IPython import display


class DataStory:

    def __init__(self, name: str):
        self._name = name
        self._views = []

    def header(self, content: str, level: int = 1):
        self._views.append({
            "type": "header",
            "spec": {
                "content": content,
                "level": level
            }
        })

    def markdown(self, md: str):
        self._views.append({
            "type": "markdown",
            "spec": {
                "content": md
            }
        })

    def plotly(self, fig: plotly.graph_objs.Figure):
        self._views.append({
            "type": "plotly",
            "spec": json.loads(fig.to_json())
        })

    def vega(self, fig: str):
        self._views.append({
            "type": "vega",
            "spec": json.loads(fig)
        })

    def _to_dict(self) -> dict:
        return {
            "name": self._name,
            "views": [view for view in self._views]
        }

    def publish(self, url: str = None) -> str:
        if not url:
            url = os.getenv("DATASTORY_URL", "http://localhost:8080/api")

        res = requests.post(url+"/story", json=self._to_dict())
        res.raise_for_status()
        
        try:
            url = res.json()["url"]
        except KeyError as e:
            return f"invalid api response {e.__str__}"

        if not webbrowser.open(url):
            display.display(display.Javascript('window.open("{url}");'.format(url=url)))

        return url

    def update(self, token: str, url: str=None) -> str:
        if not url:
            url = os.getenv("DATASTORY_URL", "http://localhost:8080/api")

        res = requests.put(f"{url}/story", json=self._to_dict(),
                           headers={"Authorization": f"Bearer {token}"})
        res.raise_for_status()

        try:
            url = res.json()["url"]
        except KeyError as e:
            return f"invalid api response {e.__str__}"

        return f"{url}/story/{res.json()['id']}"
