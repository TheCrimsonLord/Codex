from datetime import timedelta

num_list = "zero,one,two,three,four,five,six,seven,eight,nine".split(",")


def discord_number_emojis(num: int):
    return "".join(f":{num_list[int(n)]}:" for n in str(num))


def dhm_notation(td: timedelta, sep="", full=False):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    return sep.join([f"{td.days}{'days' if full else 'd'}",
                     f"{hours}{'hours' if full else 'h'}",
                     f"{minutes}{'minutes' if full else 'm'}"])
