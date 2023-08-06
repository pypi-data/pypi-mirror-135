from src.three_commas.model import BotEvent, DealShow#, BotShow
from src.three_commas.model.generated_models import BotShow
import json


def test_bot_events_are_parsed():
    filepath = 'test/sample_data/bots/btc/bot_show_with_events_btc.json'
    # filepath = './sample_data/bots/btc/bot_show_with_events_btc.json'
    with open(filepath, 'r+') as f:
        bot_show: BotShow = BotShow.of(json.loads(f.read()))

        assert isinstance(bot_show.get_bot_events()[0], BotEvent)
        assert isinstance(bot_show.get_active_deals()[0], DealShow)
