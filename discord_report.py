import argparse
from datetime import datetime
from typing import cast, List
from dateutil import tz
import discord
import pandas as pd
import sys

from sentiment import get_sentiment

def parse_args():
	parser = argparse.ArgumentParser(description="generate a health report for a guild")
	parser.add_argument("--guild", "-g", dest="guild_id", nargs=1, type=int, required=True,
		help="guild to be diagnosed")
	parser.add_argument("--output", "-o", dest="output_path", nargs=1, type=str, default="report.csv",
		help="output file path")
	parser.add_argument("--command-prefixes", "-p", dest="command_prefixes", nargs="*", type=str,
		help="command prefixes (commands will be ignored)")
	parser.add_argument("--token", "-t", dest="token", nargs=1, type=str, required=True,
		help="Discord bot token")
	return parser.parse_args(sys.argv[1:])

class MessageInfo():
	def __init__(self, message_id: int, timestamp: datetime, message: str, sentiment: float):
		self.message_id = message_id
		self.timestamp = timestamp
		self.message = message
		self.sentiment = sentiment
	
	def as_dict(self):
		return { "message_id": self.message_id, "timestamp": self.timestamp, "message": self.message, "sentiment": self.sentiment }

class DiscordReport(discord.Client):
	def __init__(self, guild_id: int, output_path: str, command_prefixes: List[str], intents: discord.Intents=discord.Intents.default()):
		super().__init__(max_messages=None, member_cache_flags=discord.MemberCacheFlags.none(), intents=intents)
		self.guild_id = guild_id
		self.output_path = output_path
		self.command_prefixes = command_prefixes

	def get_guild_guaranteed(self, guild_id: int) -> discord.Guild:
		guild = self.get_guild(guild_id)
		if guild is None:
			raise LookupError("guild not found")
		return guild

	async def on_ready(self):
		print("Generating report for guild %d..." % self.guild_id)
		guild = self.get_guild_guaranteed(self.guild_id)
		today = datetime.utcnow().date()
		day_start = datetime(today.year, today.month, today.day)
		message_infos: "List[MessageInfo]" = []
		for _, channel in enumerate(guild.text_channels):
			messages = channel.history(limit=None, after=day_start)
			async for unk_message in messages:
				message = cast(discord.Message, unk_message)
				author = cast(discord.User, message.author)
				if message.content == "" or author.bot:
					continue
				has_prefix = False
				for prefix in self.command_prefixes:
					if message.content.startswith(prefix):
						has_prefix = True
				if has_prefix:
					continue
				sentiment = get_sentiment(message.content)
				message_infos.append(MessageInfo(message.id, message.created_at, message.content, sentiment))
		df = pd.DataFrame([message_info.as_dict() for message_info in message_infos])
		df.to_csv(self.output_path, index=False, index_label="message_id")
		await self.logout()
		await self.close()

def main():
	args = parse_args()
	dr_intents = discord.Intents.none()
	dr_intents.guilds = True
	dr_intents.guild_messages = True
	dr_intents.members = True
	client = DiscordReport(args.guild_id[0], args.output_path, args.command_prefixes, intents=dr_intents)
	client.run(args.token[0])

if __name__ == "__main__":
	main()
