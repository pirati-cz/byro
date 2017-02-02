#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

__all__ = ["BRedmine", "RedmineData"]

import re
import sys
import pickle
import datetime
from redmine import Redmine
from byro.utils import Utils


class NoRefundanceField(Exception):
	pass


class BRedmine:
	"""
	Wrapper for Redmine API for Byro
	"""

	def __init__(self, user, baseUrl, projectName, **kwargs):
		"""
		:param user: user in redmine
		:param baseUrl: base url of redmine instance, like http://redmine.example.com
		:type baseUrl: string
		:param projectName: name of project (multiple project are not allowed)
		:param month: str default is last
		:param ssl: bool verify ssl certificate?
		"""
		month = kwargs.get('month', 'last')
		ssl_verify = kwargs.get('ssl', False)
		year = int(kwargs.get('year', datetime.date.today().year))
		self.refundace = kwargs.get('refundace', True)
		self.baseUrl = baseUrl
		self.interval = Utils.define_interval(month, year=year)
		self.redmine = None
		try:
			self.redmine = Redmine(self.baseUrl, requests={'verify': ssl_verify})
		except Exception as e:
			print("Nelze se připojit k Redmine :(: %s" % e )
			exit()
		self.user = self.get_user(user)
		self.project = self.redmine.project.get(projectName)

	def get_data(self):
		try:
			times = self.redmine.time_entry.filter(
				project_id= self.project.id,
				user_id= self.user.id,
				from_date= self.interval[0],
				to_date= self.interval[1]
			)
			return RedmineData(times, self)
		except NoRefundanceField:
			text = """
Data neobsahují žádné záznamy s refundací.
	Uživatel: %s %s (id: %s)
	Interval: %s (%s až %s)
Výčetku nelze vygenerovat.
			""" % (self.user.firstname, self.user.lastname, self.user.id, self.interval[2], self.interval[0], self.interval[1])
			print(text, file=sys.stderr)
			exit()

	def get_user(self, user):
		if isinstance(user, str):
			# TODO: by mail
			# user_struct = self.redmine.user.filter(name = user, limit=1)
			user_struct = self.redmine.user.get(int(user))
		elif isinstance(user, int):
			user_struct = self.redmine.user.get(user)
		else:
			raise ValueError("User must be string or int (id)")

		return user_struct


class RedmineData:
	"""
	Organizes data from Redmine API	into structure suitable for Byro
	"""

	def __init__(self, data, otherInfo):
		# prepare types of refundace
		refundace = {record.custom_fields[0].value for record in data if record.custom_fields[0].name == 'Refundace' and record.custom_fields[0].value != ''}
		if len(refundace) == 0:
			raise NoRefundanceField('Custom field [0] is not "Refundace"')

		self.refunds = {}
		self.totalSum = 0
		hours = lambda x: x.hours
		pattern = '([a-zA-Z]{1,2}\)) .*'

		for ref in refundace:
			try:
				l = re.search(pattern, ref).groups()[0]
			except AttributeError as e:
				print(ref)
				exit()
			self.refunds[l] = {'fullname': ref}
			self.refunds[l]['data'] = [ record for record in data if record.custom_fields[0].value == ref ]
			self.refunds[l]['sum'] = sum(list(map(hours, self.refunds[l]['data'])))
			self.totalSum += self.refunds[l]['sum']

		self.user = otherInfo.user
		self.project = otherInfo.project
		self.interval = (otherInfo.interval[0], otherInfo.interval[1])
		self.month = otherInfo.interval[2]
		self.year = self.interval[0].year

	def export_to_bin_file(self, filename):
		# todo: check if file exists

		with open(filename, 'wb') as f:
			pickle.dump(self, f)

		print('Data exported to file: %s' % filename)

	@staticmethod
	def import_from_bin_file(filename):
		with open(filename, 'rb') as f:
			o = pickle.load(f)

		return o
