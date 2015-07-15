# coding=utf-8
import pytest, os, sys

lib_path = os.path.abspath(os.path.join('..', 'next-word-predictor'))
sys.path.append(lib_path)

test = True
from models.tokenizer import Tokenizer

@pytest.fixture
def tokenizer():
    tokenizer = Tokenizer()
    return tokenizer

def test_strip_special_characters(tokenizer):
  test_str0 = u"[s1]s2“s3„s4#s5$s6%s7&s8\s9's10"
  test_str1 = u'"s1(s2)s3*s4+s5,s6/s7:s8;s9<s10'
  test_str2 = u"€s1=s2>s3@s4^s5_s6-s7–s8»s9«s10"

  res0 = tokenizer.strip_special_characters(test_str0)
  res1 = tokenizer.strip_special_characters(test_str1)
  res2 = tokenizer.strip_special_characters(test_str2)

  clean = " s1 s2 s3 s4 s5 s6 s7 s8 s9 s10"

  assert res0 == clean
  assert res1 == clean
  assert res2 == clean

def test_find_sentence_boundaires(tokenizer):
  test_with_dot = """Normaler Satz. Neuer Satz.
  Staz in Zeile 2. Satz nach und vor Nummer. 1 Satz <abbrevation>. <abbrevation> Satz."""
  test_with_excl = """Normaler Satz! Neuer Satz!
  Staz in Zeile 2! Satz nach und vor Nummer! 1 Satz <abbrevation>! <abbrevation> Satz!"""
  test_with_question = """Normaler Satz? Neuer Satz?
  Staz in Zeile 2? Satz nach und vor Nummer? 1 Satz <abbrevation>? <abbrevation> Satz?"""

  assumption = """Normaler Satz <S/> Neuer Satz <S/> 
  Staz in Zeile 2 <S/> Satz nach und vor Nummer <S/> 1 Satz <abbrevation> <S/> <abbrevation> Satz <S/> """

  res_dot      = tokenizer.find_sentence_boundaires(test_with_dot)
  res_excl     = tokenizer.find_sentence_boundaires(test_with_excl)
  res_question = tokenizer.find_sentence_boundaires(test_with_question)

  assert res_dot      == assumption
  assert res_excl     == assumption
  assert res_question == assumption

def test_replace_numbers(tokenizer):
  test_str = "word1234567890word"
  assert tokenizer.replace_numbers(test_str) == "word <number> word"

def test_replace_abbreviations(tokenizer):
  test_str0  = u"Abs. str1 Abschn. str2 Abt. str3 a. d. str4 Adr. str5"
  test_str1  = u"allg. str1 Anh. str2 Anm. str3 ao. str4 a. o. str5"
  test_str2  = u"Art. str1 Bd. str2 Bez. str3 bez. str4 bzw. str5" 
  test_str3  = u"dgl. str1 d. h. str2 d. j. str3 d. M. str4 dz. str5"
  test_str4  = u"ev. str1 röm-kath. str2 evtl. str3 f. str4 ff. str5" 
  test_str5  = u"gem. str1 h. c. str2 i. allg. str3 i. r. str4 Jg. str5" 
  test_str6  = u"Jgg. str1 lfd. str2 Kap. str3 Nr. str4 o. Ä. str5" 
  test_str7  = u"p. A. str1 pp. str2 ppa. str3 prov. str4 tfxu. str5"
  test_str8  = u"a. str1 u. a. str2 u. A. str3 u. a. m. str4 u. Ä. str5"
  test_str9  = u"u. d. Ä. str1 u. dgl. str2 usf. str3 usw. str4 z. t. str5"
  test_str10 = u"zz. str1 z. B. str2"

  asspumtion0 = u" <abbrevation>  str1  <abbrevation>  str2  <abbrevation>  str3  <abbrevation>  str4  <abbrevation>  str5"
  asspumtion1 = u" <abbrevation>  str1  <abbrevation>  str2"

  assert asspumtion0 == tokenizer.replace_abbreviations(test_str0)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str1)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str2)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str3)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str4)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str5)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str6)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str7)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str8)
  assert asspumtion0 == tokenizer.replace_abbreviations(test_str9)
  assert asspumtion1 == tokenizer.replace_abbreviations(test_str10)

def test_replace_unkown(tokenizer):
  test_str = "Ein Satz i mit z kurzen Wörtern"
  assert tokenizer.replace_unkown(test_str) == "Ein Satz  <unkown>  mit  <unkown>  kurzen Wörtern"