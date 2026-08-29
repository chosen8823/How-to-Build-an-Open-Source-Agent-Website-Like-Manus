from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EnvironmentSnapshot:
    environment_name: str
    python_version: str
    packages: List[Dict[str, str]]  # [{name, version}]


@dataclass
class Artifact:
    artifact_id: str
    filename: str
    root_frame_id: str
    frame_id: str
    is_user_upload: bool
    version_id: str
    content_type: str
    agent_name: str
    extracted_code: str
    lineage_messages: List[Dict]  # [{role, content}]
    environment_snapshot: EnvironmentSnapshot
    storage_path: str


@dataclass
class Frame:
    id: str
    parent_frame_id: Optional[str]
    root_frame_id: str
    agent_name: str
    status: str  # "completed", "running", "failed"
    input_data: Dict
    output_data: Dict
    child_frames: List['Frame'] = field(default_factory=list)


@dataclass
class FrameTree:
    root_frame: Frame
    artifacts: List[Artifact]
    folders: List[Dict]
