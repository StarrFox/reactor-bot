#!/usr/bin/env python3

from reactor_bot import emoji_utils as emoji

from datetime import date

from freezegun import freeze_time

NON_HOLIDAY = date(2017, 3, 27)
APRIL_FOOLS = date(2017, 4, 1)
FIVE_NINE = date(2017, 5, 9)
HALLOWEEN = date(2017, 10, 31)

EASTER_EGG_EMOJI = {
	APRIL_FOOLS: {'🦑', '\N{octopus}'},
	FIVE_NINE: {':fsociety:376935242029727745'},
	HALLOWEEN: {'\N{jack-o-lantern}', '\N{ghost}'}}

def test_get_poll_emoji():
	# TODO more test cases
	messages = {
		'poll: What should we eat for lunch?\n'
		'M)-ystery meat\n'
		'🐕 dog sandwiches\n'
		'\n'
		'3 blind mice\n'
		'🇺🇸) flags\n'
		'foo\n'
		'bar': ('🇲', '🐕', '3⃣', '🇺🇸', 'foo', 'bar'),

		'poll: Haskell lang best lang?': ('👍', '👎')}

	for date, easter_egg_emoji in EASTER_EGG_EMOJI.items():
		with freeze_time(date):
			for message, reactions in messages.items():
				poll_emoji = tuple(emoji.get_poll_emoji(message))
				# skip the easter egg emoji
				assert (poll_emoji[:-1]
					== reactions + (emoji.END_OF_POLL_EMOJI, '🤷',))
				assert poll_emoji[-1] in easter_egg_emoji

def test_extract_emoji():
	lines_and_emojis = {
		' M)-ystery meat': 'M',
		'🐕 dog sandwiches': '🐕',
		'3 blind mice': '3',
		'🇺🇸 flags': '🇺🇸',
		'<:python3:232720527448342530> python3!': '<:python3:232720527448342530>'}

	for input, output in lines_and_emojis.items():
		assert emoji.extract_emoji(input) == output

def test_parse_emoji():
	io_map = {
		'<:python3:232720527448342530>': ':python3:232720527448342530',
		'a': '🇦',
		'0': '0⃣',
		'6': '6⃣',
		# this one's wonky--sometimes we return invalid emoji,
		# but that's ok, because Discord throws them out with an error ;)
		'asdfghjkl;': 'asdfghjkl;'}

	for input, output in io_map.items():
		print(hash(emoji.parse_emoji(input)))
		print(hash(output))
		assert emoji.parse_emoji(input) == output

def test_get_letter_emoji():
	io_map = {
		'A': '🇦',
		'B': '🇧',
		'C': '🇨',
		'D': '🇩',
		'E': '🇪',
		'F': '🇫',
		'G': '🇬',
		'H': '🇭',
		'I': '🇮',
		'J': '🇯',
		'K': '🇰',
		'L': '🇱',
		'M': '🇲',
		'N': '🇳',
		'O': '🇴',
		'P': '🇵',
		'Q': '🇶',
		'R': '🇷',
		'S': '🇸',
		'T': '🇹',
		'U': '🇺',
		'V': '🇻',
		'W': '🇼',
		'X': '🇽',
		'Y': '🇾',
		'Z': '🇿'}

	# one of these tests will fail on april fools
	# (hint: it's "B")
	# unless we force the date to not be april fools
	# any date that isn't a holiday will do
	with freeze_time(NON_HOLIDAY):
		for input, output in io_map.items():
			assert emoji.get_letter_emoji(input) == output

	with freeze_time(APRIL_FOOLS):
		assert emoji.get_letter_emoji('B') == '🅱'

def test_get_digit_emoji():
	io_map = {
		'0': '0⃣',
		'1': '1⃣',
		'2': '2⃣',
		'3': '3⃣',
		'4': '4⃣',
		'5': '5⃣',
		'6': '6⃣',
		'7': '7⃣',
		'8': '8⃣',
		'9': '9⃣'}

	for input, output in io_map.items():
		assert emoji.get_digit_emoji(input) == output

def test_easter_egg_emoji():
	for date, easter_egg_emoji in EASTER_EGG_EMOJI.items():
		with freeze_time(date):
			# get the shrug emoji 100 times on HALLOWEEN
			# there is a 1/2**100 chance that this test will fail
			responses = {emoji.get_easter_egg_emoji() for _ in range(100)}
			print(date, 'expected', *easter_egg_emoji, 'got', *responses)
			assert len(responses) == len(easter_egg_emoji) # 2 unique emoji
			# the only two responses we get should be these two
			assert len(easter_egg_emoji ^ responses) == 0
