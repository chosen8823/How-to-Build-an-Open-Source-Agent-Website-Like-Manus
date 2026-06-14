import json
import time
from typing import Dict, List, Optional
from queue import Queue

from .schema import FrameTree, Frame, Artifact, EnvironmentSnapshot


class FrameStore:
    def __init__(self):
        self.trees: Dict[str, FrameTree] = {}  # root_frame_id -> FrameTree
        self._subscribers: List[Queue] = []

    def ingest(self, raw: dict) -> FrameTree:
        """Parse the exact JSON schema from the user's proteomics example."""
        root_raw = raw['root_frame']
        root = Frame(
            id=root_raw['id'],
            parent_frame_id=root_raw.get('parent_frame_id'),
            root_frame_id=root_raw['root_frame_id'],
            agent_name=root_raw['agent_name'],
            status=root_raw['status'],
            input_data=root_raw.get('input_data', {}),
            output_data=root_raw.get('output_data', {}),
        )

        artifacts = []
        for a in raw.get('artifacts', []):
            env = a.get('environment_snapshot', {})
            artifacts.append(Artifact(
                artifact_id=a['artifact_id'],
                filename=a['filename'],
                root_frame_id=a['root_frame_id'],
                frame_id=a['frame_id'],
                is_user_upload=a.get('is_user_upload', False),
                version_id=a['version_id'],
                content_type=a['content_type'],
                agent_name=a['agent_name'],
                extracted_code=a.get('extracted_code', ''),
                lineage_messages=a.get('lineage_messages', []),
                environment_snapshot=EnvironmentSnapshot(
                    environment_name=env.get('environment_name', ''),
                    python_version=env.get('python_version', ''),
                    packages=env.get('packages', [])
                ),
                storage_path=a.get('storage_path', '')
            ))

        tree = FrameTree(
            root_frame=root,
            artifacts=artifacts,
            folders=raw.get('folders', [])
        )
        self.trees[root.id] = tree
        self._broadcast({
            'type': 'tree_ingested',
            'root_frame_id': root.id,
            'agent_name': root.agent_name
        })
        return tree

    def subscribe(self) -> Queue:
        q = Queue()
        self._subscribers.append(q)
        return q

    def _broadcast(self, event: dict):
        dead = []
        for q in self._subscribers:
            try:
                q.put_nowait(json.dumps(event))
            except Exception:
                dead.append(q)
        for q in dead:
            self._subscribers.remove(q)


_store = FrameStore()


def get_store() -> FrameStore:
    return _store
