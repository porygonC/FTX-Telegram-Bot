

def get_rr(tp, sl, price, side):
    if not tp or not sl:
        return 'none'
    else:
        return round((tp - price) / (price - sl), 2) if side == 'BUY' else round((price - tp) / (sl - price), 3)


def get_message_text_futures(position, tp, sl, symbol, side, price) -> str:
    if position['size'] == 0:
        return f'Position closed:\n-------------------------\n{symbol} @ {price}'
    rr = get_rr(tp, sl, price, side)
    return f'New order filled:\n----------------------------\n{side} {symbol} \
                \nEntry price: {price}\nSL: {sl} | TP: {tp}\nRisk/reward: {rr}'


def get_message_text_spot(tp, sl, symbol, side, price) -> str:
    rr = get_rr(tp, sl, price, side)
    return f'New order filled:\n----------------------------\n{side} {symbol} \
                            \nEntry price: {price}\nSL: {sl} | TP: {tp}\nRisk/reward: {rr}'
