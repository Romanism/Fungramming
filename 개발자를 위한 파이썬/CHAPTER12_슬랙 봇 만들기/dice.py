# bot이 반응할 수 있게 하는 데코레이터 함수를 불러옵니다.
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.dispatcher import Message

# 무엇에 반응할지 잡아줄 수 있는 re(정규표현식) 패키지를 불러옵니다.
import re

# listen_to는 채널에서 오가는 모든 대화에 반응합니다.
# 데코레이터 함수의 첫 번째 피라미터는 정규 표현식이고 두 번째 파라미터는 플래그입니다.
@listen_to("Hello", re.IGNORECASE)

# 첫번째 파라미터는 디스패처의 메시지 클래스 입니다.
# 반응해야 할 채널에 메시지를 보내는 함수 등이 있습니다.
# 여기 없는 두 번째 이후의 파라미터는 앞 정규 표현식에 그룹이 있으면 매칭된 문자열이 들어갑니다.
# 개수는 상한이 없습니다. 그룹 숫자에 따라 파라미터를 더 늘리면 됩니다.
def hello(msg: Message):
    # send는 채널에 그냥 말합니다.
    msg.send("World!!")

# respond_to는 @을 이용해서 멘션했을 경우에만 반응합니다.
# 나머지는 listen_to의 역할과 같습니다.
@respond_to("Hi", re.IGNORECASE)

def hi(msg: Message):
    # reply는 해당 반응을 일으킨 사람에게 말합니다.
    # listen_to든 respond_to든 말을 건 사람에게 대답합니다.
    msg.reply("Thank you 39!!")
