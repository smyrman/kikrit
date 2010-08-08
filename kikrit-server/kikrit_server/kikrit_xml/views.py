# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_resoponse

from accounts import RFIDCard, Account, deposit_to_account,\
		withdraw_from_account, purchase_from_account
from merchnadise import Merchnadise, buy_merchandise

def error(status):
	MSGS = {
			"000":"OK",
			"100":"NOT FOUND",
			"101":"ACCOUNT NOT FOUND",
			"102":"RFID CARD NOT FOUND",
			"103":"MERCHANDISE NOT FOUND",
			"200":"ACCESS DENIED",
			"201":"TRANSACTION DENIED",
			"202":"PURCHACE DENIED",
			"299":"YOU HAVE BEEN DENIED BECAUSE YOU ARE STUPID",
			"300":"SERVER ERROR",
			"301":"CLIENT AUTHENTICATION ERROR",
			"302":"INVALID REQUEST",
	}
	# Render:
	t = "kikrit_xml/error.xml"
	d = {"status":status, "msg":MSGS["%.3d"%status]}
	return render_to_response(t, d)


# FIXME: INsert clinet authentication decorators for all functions except
# error.

def merchandises(request, post_str):
	# Render:
	t = "kikrit_xml/merchandises.xml"
	d = {"merchandises": Merchandise.objects.all()}
	return render_to_response(t, d)


def account(request, post_str):
	# Get account:
	account = None
	if "rfid" in request.POST.keys():
		try:
			rfid_card = RFIDCard.objects.get(rfid_string=request.POST["rfid"])
		except RFIDCard.DoesNotExist:
			return error(102)
		account = rfid_card.account
	else:
		try:
			account = Account.objects.get(id=request.POST["account_id"])
		except Account.DoesNotExis:
			account = None

	if account == None:
		return error(101)

	# Render:
	t = "kikrit_xml/account.xml"
	d = {"account": account}
	return render_to_response(t, d)


def transaction(request, post_str):
	# Get account:
	account = None
	if "rfid" in request.POST.keys():
		try:
			rfid_card = RFIDCard.objects.get(rfid_string=request.POST["rfid"])
		except RFIDCard.DoesNotExist:
			return error(102)
		account = rfid_card.account
	else:
		try:
			account = Account.objects.get(id=request.POST["account_id"])
		except Account.DoesNotExis:
			account = None
	if account == None:
		return error(101)

	# Get transaction:
	transaction = None
	if request.POST["type"] == "purchace":
		if "merchandises" in request.POST:
			m_ids = request.POST["merchandises"].split(',')
			merchandises = []
			for m_id in mids:
				try:
					merchandises.append(Merchandise.objects.get(id=m_id))
				except Merchandise.DoesNotExist:
					return error(103)
			transaction = buy_merchandise(account, merchandises)
		else:
			amount = request.POST["amount"]
			transaction = purchase_from_account(account, amount, None)
		if transation == None:
			return error(202)
	elif request.POST["type"] == "withdraw":
		amount = request.POST["amount"]
		transaction = withdraw_from_account(account, amount, None)
	elif request.POST["type"] == "deposit":
		amount = request.POST["amount"]
		transaction = deposit_to_account(account, amount, None)

	# Render:
	t = "kikrit_xml/transaction.xml"
	d = {"account":account, "transaction":transaction}
	return render_to_response(t, d)
