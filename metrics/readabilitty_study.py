# https://www.numpy.org/
# pip install --user numpy

'''A library with implementations of readability formulas'''

import numpy as np


__all__ = ['cli', 'fkgl', 'fre', 'smog', 'gfi', 'forcast', 'ari']

def cli(mccphw: float, mscphw: float) -> float:
	'''Coleman-Liau Index

	Arguments:
		mccphw: mean character count per hundred words
		mscphw: mean sentence count per hundred words

	Returns:
		float:  The coleman liau index
	'''
	return (0.0588 * mccphw) - (0.296 * mscphw) - 15.8

def fkgl(mwcps: float, msylcpw: float) -> float:
	'''Flesch-Kincaid Grade Level

	Arguments:
		mwcps:    mean word count per sentence
		msylcpw:  mean syllable count per word

	Returns:
		float:  The flesch-kincaid grade level
	'''
	return (0.39 * mwcps) + (11.8 * msylcpw) - 15.59

def fre(msylcpw: float, mwcps: float, sc: float) -> float:
	'''Flesch Reading Ease

	Arguments:
		msylcpw:  mean syllable count per word
		mwcps:    mean word count per sentence
		sc:       sentence count

	Returns:
		float:  Flesch reading ease score
	'''
	return 206.835 - (84.6 * (msylcpw / mwcps)) - (1.015 * (mwcps / sc))

def smog(psylc: float, sc: float) -> float:
	'''Simple Measure of Gobbledygook

	Arguments:
		psylc:  polysyllable count
		sc:     sentence count

	Returns:
		float:  Smog score
	'''
	return (1.043 * np.sqrt(psylc * (30 / sc))) + 3.1291

def gfi(wc: float, sc: float, psylc: float) -> float:
	'''Gunning Fog Index

	Arguments:
		wc:     word count
		sc:     sentence count
		psylc:  polysyllable count

	Returns:
		float:  Gunning fog index
	'''
	return 0.4 * ((wc / sc) + ((psylc / wc) * 100))

def forcast(sscifs: float) -> float:
	'''Forcast formula

	Arguments:
		sscifs: single syllable count in a text sample of X words

	Returns:
		float:  Forcast formula
	'''
	return 20 - (sscifs / 10)

def ari(anc: float, wc: float, sc: float) -> float:
	'''Automated Readability Index

	Arguments:
		anc:  alphanumeric characters count
		wc:   word count
		sc:   sentence count

	Returns:
		float:  Automated Readability Index
	'''
	return 4.71 * (anc / wc) + 0.5 * (wc / sc) - 21.43

def ndc(vwc: float, wc: float, mwcps: float) -> float:
	'''New Dale-Chall formula

	Arguments:
		vwc:    easy vocabulary word count
		wc:     word count
		mwcps:  mean word count per sentence

	Returns:
		float:  New Dale-Chall score
	'''
	# percentage of difficult words
	pdw = (wc - vwc) / wc
	score = 0.1579 * (pdw  * 100) + 0.0496 * mwcps
	if pdw > 0.05:
		return score + 3.6365
	return score

def nfc(ewcphw: float, hwcphw: float, scphw: float) -> float:
	'''New Fog Count

	Arguments:
		ewcphw: easy word count (2 or less syllables) per hundred words
		hwcphw: hard word count (3 or more syllables) per hundred words
		scphw:  sentence count per hundred words

	Returns:
		float:  New Fog Count score
	'''
	return (((ewcphw + (3 * hwcphw)) / scphw) - 3) / 2