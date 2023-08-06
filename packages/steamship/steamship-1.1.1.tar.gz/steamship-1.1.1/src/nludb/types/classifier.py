from typing import List
from dataclasses import dataclass
from nludb.types.base import NludbRequest, NludbResponse
from nludb.types.search import Hit

@dataclass
class ClassifierCreateRequest(NludbRequest):
  model: str
  name: str = None
  upsert: bool = True
  save: bool = True
  labels: List[str] = None

@dataclass
class ClassifierCreateResponse(NludbResponse):
  classifierId: str = None

  @staticmethod
  def safely_from_dict(d: any) -> "ClassifierCreateResponse":
    return ClassifierCreateResponse(
      classifierId = d.get('classifierId', None),
    )

@dataclass
class ClassifyRequest(NludbRequest):
  docs: List[str]
  classifierId: str = None
  model: str = None
  labels: List[str] = None
  k: int = None

@dataclass
class ClassifyResponse(NludbResponse):
  classifierId: str = None
  model: str = None
  hits: List[List[Hit]] = None

  @staticmethod
  def safely_from_dict(d: any) -> "ClassifyResponse":
    hits = [[Hit.safely_from_dict(h) for h in innerList] for innerList in d.get("hits", [])]
    return ClassifyResponse(
      classifierId = d.get('classifierId', None),
      model = d.get('model', None),
      hits = hits
    )

@dataclass
class LabelInsertRequest(NludbRequest):
  value: str
  externalId: str = None
  externalType: str = None
  metadata: str = None

@dataclass
class LabelInsertResponse(NludbResponse):
  labelId: str
  value: str
  externalId: str = None
  externalType: str = None
  metadata: str = None

  @staticmethod
  def safely_from_dict(d: any) -> "LabelInsertResponse":
    return LabelInsertResponse(
      labelId = d.get('labelId', None),
      value = d.get('value', None),
      externalId = d.get('externalId', None),
      externalType = d.get('externalType', None),
      metadata = d.get('metadata', None),
    )

@dataclass
class ClassifierDeleteResponse(NludbResponse):
  classifierId: str = None

  @staticmethod
  def safely_from_dict(d: any) -> "ClassifierDeleteResponse":
    return ClassifierDeleteResponse(
      classifierId = d.get('classifierId', None),
    )
