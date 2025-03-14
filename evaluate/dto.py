import json
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional
from typing import List


@dataclass
class SimpleAskMethod:
    id: str
    name: str
    category: str
    type: int
    hitSituationType: int
    recognizePoint: int
    recognizePointDesc: str
    score: float
    rewriteQuestion: str

@dataclass
class SimpleScene:
    id: str
    type: int
    name: Optional[str]
    lightOn: bool
    dutyOpen: bool

@dataclass
class TurnHuman:
    required: bool
    reason: str

@dataclass
class Video:
    url: str
    coverUrl: str

@dataclass
class DelayAnswer:
    delayInSec: int
    content: str
    memes: List[str]
    images: List[str]
    videos: List[Video]

@dataclass
class ResultAnswer:
    content: str
    memes: List[str]
    images: List[str]
    videos: List[Video]
    delayAnswers: List[DelayAnswer]

@dataclass
class FocusInfo:
    spuId: str
    spuDetailUrl: str
    spuImageUrl: str
    spuName: str
    skuId: str
    skuIdName: str
    orderId: str
    orderStatus: str

@dataclass
class AnswerRsp:
    originQuestion: str
    rewriteQuestion: str
    askMethod: SimpleAskMethod
    scene: SimpleScene
    answer: ResultAnswer
    turnHuman: TurnHuman
    focusInfo: FocusInfo
    stateInfo: dict
    recallAskMethodNameList: []
    rerankAskMethodNameList: []

@dataclass
class QuestionReq:
    chatbotShopId: str
    question: str
    mockAnswers: list[str]  # 默认参数

    def to_json(self):
        return json.dumps({
            "chatbotShopId": self.chatbotShopId,
            "question": self.question,
            "mockAnswers": self.mockAnswers
        }, ensure_ascii=False, indent=4)


T = TypeVar('T')

@dataclass
class BaseResult(Generic[T]):
    FAILED = 0
    SUCCESS = 1
    SUCCESS_MSG = "操作成功!"
    FAILED_MSG = "操作失败!"

    code: int
    msg: str
    data: Optional[T] = None

    def __init__(self, code: int, msg: str, data: Optional[T] = None):
        self.code = code
        self.msg = msg
        self.data = data

    @classmethod
    def success(cls, data: T):
        return cls(cls.SUCCESS, cls.SUCCESS_MSG, data)

    @classmethod
    def fail(cls, msg: str):
        return cls(cls.FAILED, msg, None)

    def is_success(self) -> bool:
        return self.code == self.SUCCESS
